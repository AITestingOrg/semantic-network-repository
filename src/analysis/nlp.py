import spacy
from spacy import displacy
from .algorithms.subject_object_extraction import findSVOs

nlp = spacy.load('en')

class NLP:
    def find_useful_stuff(self, text):
        output = {}
        output['text'] = text
        parsedData = nlp(text)

        # Lexicon
        output['lexicon'] = []
        for token in parsedData:
            output['lexicon'].append(' '.join([token.orth_, token.pos_, token.lemma_]))

        # Dependencies
        output['dependencies'] = []
        for token in parsedData:
            output['dependencies'].append(' '.join([token.orth_, token.dep_, token.head.orth_, ' '.join([t.orth_ for t in token.lefts]), ' '.join([t.orth_ for t in token.rights])]))

        # Entities
        output['entities'] = []
        ents = list(parsedData.ents)
        for entity in ents:
            output['entities'].append(' '.join([entity.label, entity.label_, ' '.join(t.orth_ for t in entity)]))

        # Find all the subject verb pairs
        output['svos'] = []
        output['svos'].append(findSVOs(parsedData))

        # Display graph
        output['svgs'] = []
        output['svgs'].append(displacy.render(parsedData, style='dep'))
        output['svgs'].append(displacy.render(parsedData, style='ent'))

        return output