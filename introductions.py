import sys


class Introduction(object):
    indirectColor = '0.650 0.700 0.700'
    def __init__(self, src, dst, direct=True):
        self.src = src
        self.dst = dst
        self.direct = direct
        if ('isConference' not in src.categories and
            'isConference' not in dst.categories):
            src.linkedin = dst.linkedin = True

    def excludedBy(self, excludedCategories):
        return (self.src.excludedBy(excludedCategories) or
                self.dst.excludedBy(excludedCategories))

    def __str__(self):
        color = ''
        if not self.direct:
            color = self.indirectColor
        if color:
            color = ' [color="%s"]' % color
        return '"%s" -> "%s"%s;' % (self.src.name, self.dst.name, color)


class Person(object):
    colors = {
        'inPerson' : 'darkseagreen',
        'unmet' : 'yellow',
        'inEmail' : 'orange',
        'onPhone' : 'greenyellow',
        'isConference' : 'green',
        }

    def __init__(self, name, *categories):
        self.name = name
        self.categories = categories or ['inPerson']
        self.linkedin = False

    def excludedBy(self, excludedCategories):
        for ex in excludedCategories:
            if ex in self.categories:
                return True
        return False

    def __str__(self):
        if len(self.categories) == 1 and self.categories[0] in self.colors:
            color = ' [color="%s" style=filled]' % (
                self.colors[self.categories[0]])
        else:
            color = ''
        return '"%s"%s;' % (self.name, color)


class Group(object):
    '''A group of people all met at the same time.'''
    def __init__(self, *people):
        self.people = people

    def add(self, person):
        self.people.append(person)

    def __len__(self):
        return len(self.people)

    def str(self, excludedCategories):
        included = []
        for person in self.people:
            if not person.excludedBy(excludedCategories):
                included.append(person)
        if included:
            return '{ rank="same"; %s ;}' % (
                ' '.join('"%s"' % p.name for p in included))


class Graph(object):
    def __init__(self):
        self.names = {}
        self.people = []
        self.introductions = []
        self.groups = []

    def add(self, name, *categories):
        assert name not in self.names, "Name '%s' added more than once." % name
        self.names[name] = None
        p = Person(name, *categories)
        self.people.append(p)
        return p

    def intro(self, src, dst, **kw):
        self.introductions.append(Introduction(src, dst, **kw))

    def group(self, *people):
        self.groups.append(Group(*people))

    def str(self, excludedCategories=None, showSingletons=True):
        if excludedCategories is None:
            excludedCategories = []
        s = ['digraph intros {',
             # 'node [color=lightblue2, style=filled];',
             # 'graph [drankdir=TB]',
             # 'graph [overlap=scale]',
             # 'graph [packMode="clust"];',
             'graph [ratio="compress"];',
             'graph [splines=true];',
             'graph [K=1];',
             'graph [overlap="9:porthoyx"];',
             'graph [packMode="node"];',

             # Looks terrible, all overlapping:
             # 'graph [overlap=vpsc];',

             # Causes splines to go away, and edges to overlap nodes:
             # 'graph [sep=0.05]',
             ]
        peopleCount = 0
        for person in self.people:
            if (not person.excludedBy(excludedCategories) and
                (showSingletons or person.linkedin)):
                peopleCount += 1
                s.append(str(person))
        introCount = 0
        for intro in self.introductions:
            if not intro.excludedBy(excludedCategories):
                introCount += 1
                s.append(str(intro))
        for group in self.groups:
            strGroup = group.str(excludedCategories)
            if strGroup:
                s.append(strGroup)
        s.append('}')
        print >>sys.stderr, "Processed %d people, %d introductions" % (
            peopleCount, introCount)
        return '\n'.join(s)
