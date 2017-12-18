import spacy
from spacy import displacy

from ..common.models.node import Node
from .algorithms.subject_object_extraction import findSVOs
from ..common.persitence.wrapper_factory import WrapperFactory

nlp = spacy.load('en')
state = {}

class NLP:
    def __init__(self):
        self.db = WrapperFactory.build_neo4j_wrapper('localhost', 7687, 'neo4j', 'test')

    def find_useful_stuff(self, text, debug = False):
        output = {}
        output['text'] = text
        if len(text.split(' ')) == 1:
            ideas = self.db.get_direct_relations(text.strip())
            related_nodes = {}
            for idea in ideas.records():
                if idea['r'].type not in related_nodes:
                    related_nodes[idea['r'].type] = []
                related_nodes[idea['r'].type].append(idea['node'].properties['name'])
            output['ideas'] = related_nodes
            return output

        parsedData = nlp(text)

        for sent in parsedData.sents:
            sent = ''.join(sent.string.strip())
            if len(sent) > 3:
                sent = nlp(sent)
                self.process_sentence(sent, output, debug)

        return output

    def process_sentence(self, sent, output, debug):
        print('TEXT' + sent.text)
        output['structure'] = {}

        # Determine if this is a question
        output['is_question'] = self.is_question(sent)

        # Entities
        output['entities'] = self.extract_entities(sent)

        # Find all the subject verb pairs
        output['svos'] = findSVOs(sent)

        structure = {}
        for token in sent:
            if token.dep_ == 'nsubj':
                structure['nsubj'] = token.text.lower()
            if token.dep_ == 'ROOT':
                structure['root'] = token.text.lower()

        print('SVOs')
        for svo in output['svos']:
            print('\t' + str(svo))
            if output['is_question'] == False:
                if svo[0] == 'there' and svo[1] == 'is':
                    subject = svo[2]
                    node = self.db.get_node(subject)
                    if node == None:
                        self.db.insert_node(Node(subject))
                    break

            svo = nlp(' '.join(svo))
            if spacy.explain(svo[0].tag_).startswith('noun') and svo[1].lemma_ != '!':
                self.db.insert_edge(svo[0].lemma_, svo[2].lemma_, svo[1].lemma_)

        if output['is_question'] and 'nsubj' in structure and structure['nsubj'] in state and state[structure['nsubj']] == True:
            output['result'] = structure['nsubj']

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
            lexicon.append(' '.join(
                [token.orth_, spacy.explain(token.pos_), '"', spacy.explain(token.tag_), '"', '"' + token.tag_ + '"',
                 token.lemma_]))
            deps.append(' '.join(
                [token.orth_, token.dep_, token.head.orth_, ' '.join([t.orth_ for t in token.lefts]),
                 ' '.join([t.orth_ for t in token.rights])]))
        return lexicon, deps

    def extract_debug_graphs(self, parsedData):
        return [displacy.render(parsedData, style='dep'), displacy.render(parsedData, style='ent')]

    def extract_entities(self, parsedData):
        entities = []
        ents = list(parsedData.ents)
        for entity in ents:
            entities.append(
                ' '.join([str(entity.label), entity.label_, ' '.join([str(t.orth_) for t in entity])]))
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

