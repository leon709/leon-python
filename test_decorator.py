def node(name='', node_id=0, yes_func=None, no_func=None):
    def _deco(func):
        def __deco(flow):
            flow.data['nodes'].append(name if name else func.__name__)
            r = func(flow)
            if r:
                if yes_func:
                    yes_func(flow)
            else:
                if no_func:
                    no_func(flow)
        return __deco
    return _deco

class Flow(object):
    def __init__(self):
        self.data = {'nodes':[]}
        
    def t1(self):
        print('t1---')
        
    def t2(self):
        print('t2---')
        self.data['t2_data'] = 't2222'
    
    @node(yes_func=t1, no_func=t2)
    def myfunc2(self):
        print(" myfunc2() called.")
        return 0
    
    @node(node_id=3, yes_func=t1, no_func=myfunc2)
    def myfunc(self):
        print(" myfunc() called.")
        return 0
    
    def run(self):
        self.myfunc()
        print self.__class__.__name__
        print self.data

if __name__ == '__main__':
    Flow().run()
