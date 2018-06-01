import spacy
from spacy import displacy
import re

from common.models.node import Node
from analysis.algorithms.subject_object_extraction import findSVOs
from common.persitence.wrapper_factory import WrapperFactory

nlp = spacy.load('en')
state = {}

class NLP:
    def __init__(self):
        self.db = WrapperFactory.build_neo4j_wrapper('localhost', 7687, 'neo4j', 'test')
        self.nsubj = None

    def find_useful_stuff(self, text, debug = False, write = False):
        output = {}
        output['text'] = text
        if len(text.split(' ')) == 1:
            ideas = self.db.get_direct_relations(text.strip())
            related_nodes = {}
            for idea in ideas.records():
                if idea['r'].type not in related_nodes:
                    related_nodes[idea['r'].type] = []
                related_nodes[idea['r'].type].append(idea['node'].properties['name'])
            output['ideas'] = [[text.strip(), edge, ', '.join(related_nodes[edge])] for edge in related_nodes]
            return output

        parsedData = nlp(text)

        for sent in parsedData.sents:
            sent = ''.join(sent.string.strip())
            if len(sent) > 3:
                sent = nlp(sent)
                self.process_sentence(sent, output, debug, write)
        if 'structure' in output and 'nsubj' in output['structure']:
            ideas = self.db.get_direct_relations(self.nsubj.lemma_)
            related_nodes = {}
            for idea in ideas.records():
                if idea['r'].type not in related_nodes:
                    related_nodes[idea['r'].type] = []
                related_nodes[idea['r'].type].append(idea['node'].properties['name'])
            output['ideas'] = [[output['structure']['nsubj'].strip(), edge, ', '.join(related_nodes[edge])] for edge in related_nodes]
        elif re.search(r'@(\S+)', text):
            print('Found user')
            m = re.search(r'@(\S+)', text)
            print(m.group(0))
            user = m.group(0).replace('>', '')
            output['structure'] = {'nsubj': user}
            ideas = self.db.get_direct_relations(user)
            related_nodes = {}
            for idea in ideas.records():
                if idea['r'].type not in related_nodes:
                    related_nodes[idea['r'].type] = []
                related_nodes[idea['r'].type].append(idea['node'].properties['name'])
            output['ideas'] = [[output['structure']['nsubj'].strip(), edge, ', '.join(related_nodes[edge])] for edge in related_nodes]
        return output

    def process_sentence(self, sent, output, debug, write):
        print('TEXT ' + sent.text)
        output['structure'] = {}

        # Determine if this is a question
        output['is_question'] = self.is_question(sent)

        # Entities
        output['entities'] = self.extract_entities(sent)

        # Find all the subject verb pairs
        output['svos'] = findSVOs(sent)
        nsubj_exp = ''
        for token in sent:
            print(token.text.lower(), token.dep_, nsubj_exp)
            if token.dep_ == 'nsubj':
                output['structure']['nsubj'] = token.text.lower()
                self.nsubj = token
                nsubj_exp = spacy.explain(token.tag_)

                answer = self.db.get_node_from_relationship(token.lemma_, token.head.lemma_).single()
                generalized_answer = self.db.get_most_generalized_relationship(token.lemma_, token.head.lemma_)
                if generalized_answer:
                    output['gen_answer'] = ""
                    for result in generalized_answer:
                        output['gen_answer'] += result['node'].properties['name'] + ', '
                output['answer'] = answer['node'].properties['name'] if answer != None else "No"
            elif token.dep_ == 'ROOT':
                output['structure']['root'] = token.text.lower()
            elif output['is_question'] and token.dep_ == 'dobj' or \
                    output['is_question'] and \
                    token.dep_ == 'dobj' and \
                    nsubj_exp.startswith('wh-'):
                print('Looking for alternative nsubj')
                output['structure']['nsubj'] = token.lemma_
                self.nsubj = token
                output['structure']['edge'] = token.head.lemma_
                print('Querying for answer')
                answer = self.db.get_node_from_relationship(token.lemma_, token.head.lemma_).single()
                generalized_answer = self.db.get_most_generalized_relationship(token.lemma_, token.head.lemma_)
                if generalized_answer:
                    output['gen_answer'] = ""
                    for result in generalized_answer:
                        output['gen_answer'] += result['node'].properties['name'] + ', '
                output['answer'] = answer['node'].properties['name'] if answer != None else "No"

        if write:
            for svo in output['svos']:
                if output['is_question'] == False:
                    print(' '.join(svo))
                    svoParsed = nlp(' '.join(svo))
                    if spacy.explain(svoParsed[0].tag_).startswith('noun') and svoParsed[1].lemma_ != '!':
                        print('Inserting svo')
                        self.db.insert_edge(svoParsed[0].lemma_, svoParsed[2].lemma_, svoParsed[1].lemma_)

        if output['is_question'] and 'nsubj' in output['structure'] and output['structure']['nsubj'] in state and state[output['structure']['nsubj']] == True:
            output['result'] = output['structure']['nsubj']

        if debug:
            output['lexicon'] = []
            output['dependencies'] = []
            # Lexicon and Dependencies
            lexicon, deps = self.extract_debug_data(sent)
            output['lexicon'].extend(lexicon)
            output['dependencies'].extend(deps)

            # Display graph
            output['svgs'] = self.extract_debug_graphs(sent)

    def extract_debug_data(self, parsedData):
        lexicon = []
        deps = []
        for token in parsedData:
            lexicon.append(
                [token.orth_, spacy.explain(token.pos_), spacy.explain(token.tag_), token.tag_, token.lemma_])
            deps.append(
                [token.orth_, token.dep_, token.head.orth_, ' '.join([t.orth_ for t in token.lefts]),
                 ' '.join([t.orth_ for t in token.rights])])
        return lexicon, deps

    def extract_debug_graphs(self, parsedData):
        return [displacy.render(parsedData, style='dep'), displacy.render(parsedData, style='ent')]

    def extract_entities(self, parsedData):
        entities = []
        ents = list(parsedData.ents)
        for entity in ents:
            entities.append(
                [str(entity.label), entity.label_, ' '.join([str(t.orth_) for t in entity])])
        return entities

    def is_question(self, parsedData):
        # starting word is question
        is_question = True if spacy.explain(parsedData[0].tag_).startswith('wh-') else False

        # second word is not be when "when" is the first word
        if len(parsedData) > 1 and is_question:
            is_question = False if parsedData[0].lemma_ == 'when' and parsedData[1].lemma_ != 'be' else True

        if not is_question:
            is_question = True if parsedData[0].lemma_ == 'be' else False

        return is_question

