""" Portal tools specific vocabularies
"""
import operator
from utils import compare
from zope.component import getUtilitiesFor
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName

#
# portal_vocabularies
#
class PortalVocabulariesVocabulary(object):
    """ Return vocabulularies in portal_vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ See IVocabularyFactory interface
        """
        res = []
        vtool = getToolByName(context, 'portal_vocabularies', None)
        if vtool:
            vocabularies = vtool.objectValues()
            res.extend([(term.getId(), term.title_or_id())
                        for term in vocabularies])

        factories = getUtilitiesFor(IVocabularyFactory)
        res.extend([(key, key) for key, factory in factories])

        res.sort(key=operator.itemgetter(1), cmp=compare)
        res.insert(0, ('', ''))
        items = [SimpleTerm(key, key, value) for key, value in res]
        return SimpleVocabulary(items)

PortalVocabulariesVocabularyFactory = PortalVocabulariesVocabulary()

#
# portal_languages
#
class PortalLanguagesVocabulary(object):
    """ Return portal types as vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        """ See IVocabularyFactory interface
        """
        portal_languages = getToolByName(context, 'portal_languages', None)
        if not portal_languages:
            return SimpleVocabulary([])

        res = portal_languages.listSupportedLanguages()
        res = [(x, (isinstance(y, str) and y.decode('utf-8') or y))
               for x, y in res]

        res.sort(key=operator.itemgetter(1), cmp=compare)
        items = [SimpleTerm(key, key, value) for key, value in res]
        return SimpleVocabulary(items)

PortalLanguagesVocabularyFactory = PortalLanguagesVocabulary()