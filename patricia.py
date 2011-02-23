class Patricia(object):
    def __init__(self):
        self._d = {}

    def addWord(self,w):
        d = self._d
        i = 0
        while 1:
            try:
                node = d[w[i:i+1]]
            except KeyError:
                if d:
                    d[w[i:i+1]] = [w[i+1:],{}]
                else:
                    if w[i:i+1] == '':
                        return
                    else:
                        if i != 0:
                            d[''] = ['',{}]
                        d[w[i:i+1]] = [w[i+1:],{}]
                return

            i += 1
            if w.startswith(node[0],i):
                if len(w[i:]) == len(node[0]):
                    if node[1]:
                        try:
                            node[1]['']
                        except KeyError:
                            d = node[1]
                            d[''] = ['',{}]
                    return
                else:
                    i += len(node[0])
                    d = node[1]
            else:
                ii = i
                j = 0
                while ii != len(w) and j != len(node[0]) and \
                      w[ii:ii+1] == node[0][j:j+1]:
                    ii += 1
                    j += 1
                tmpd = {}
                tmpd[node[0][j:j+1]] = [node[0][j+1:],node[1]]
                tmpd[w[ii:ii+1]] = [w[ii+1:],{}]
                d[w[i-1:i]] = [node[0][:j],tmpd]
                return

    def isWord(self,w):
        d = self._d
        i = 0
        while 1:
            try:
                node = d[w[i:i+1]]
            except KeyError:
                return False
            i += 1
            if w.startswith(node[0],i):
                if len(w[i:]) == len(node[0]):
                    if node[1]:
                        try:
                            node[1]['']
                        except KeyError:
                            return False
                    return True
                else:
                    i += len(node[0])
                    d = node[1]
            else:
                return False

    def isPrefix(self,w):
        d = self._d
        i = 0
        wlen = len(w)
        while 1:
            try:
                node = d[w[i:i+1]]
            except KeyError:
                return False
            i += 1
            if w.startswith(node[0][:wlen-i],i):
                if wlen - i > len(node[0]):
                    i += len(node[0])
                    d = node[1]
                else:
                    return True
            else:
                return False

    __getitem__ = isWord
