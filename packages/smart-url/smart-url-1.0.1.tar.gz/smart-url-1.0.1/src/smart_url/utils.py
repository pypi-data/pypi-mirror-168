
class PathUtils(str):
    def __truediv__(self, other):
        """ Sum the relative paths considering the separotors """
        if self.endswith('/'):
            value = self + other.lstrip('/')
        elif other.startswith('/'):
            value = self + other
        else:
            value = self + '/' + other
        return self.__class__(self.sanitize_path(value))

    @staticmethod
    def sanitize_path(path):
        value = path.replace('//', '/').replace(' ', '')
        if not value.startswith('/'):
            value = f'/{value}'
        value = value.split('?')[0]
        value = value.split('#')[0]
        return value

    @staticmethod
    def sanitize_anchor(anchor, with_sharp=False):
        value = anchor.replace('//', '/').replace(' ', '').replace('#', '')
        if value and with_sharp and not value.startswith('#'):
            value = f'#{value}'
        return value

    @staticmethod
    def sanitize_query(query):
        if not query:
            return ''
        value = query.replace(' ', '')
        if not value.startswith('?'):
            value = f'?{value}'
        return value

    @staticmethod
    def dismember_path(path):
        query = path.split('?')
        if len(query) > 1:
            query = query[1].split('#')
            query = query[0]
        else:
            query = ''

        anchor = path.split('#')
        if len(anchor) > 1:
            anchor = anchor[1]
        else:
            anchor = ''
        return query, anchor
