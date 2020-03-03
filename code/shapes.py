class Shape:

    n = 0
    k = 0

    def __init__(self, loop ,polygon = None, c_o_m = None, name = None, radius = None):

        self.vertices = loop

        if not name:
            Shape.n += 1
            self.tag = 'p{}'.format(Shape.n)
        else:
            self.tag = name

        self.kind = polygon
        self.only_loop = not polygon
        self.r = radius
        self.unions = ''
        self.crel = []
        self.hrel = []
        self.vrel = []
        self.center = c_o_m

    def reset_n():
    
        Shape.n = 0
    
    def get_shape(self):
    
        return self.kind

    def get_center(self):
    
        return self.center
        

    def get_radius(self):

        if self.r:
            return self.r

    def get_loop(self):
    
        return self.vertices

    def get_name(self):
    
        return self.tag

    def find_unions(self, input):
    
        if self.kind == 'dot' or self.kind == 'circle':
            return

        for i in range(1, len(self.vertices)):
            for k, v in input.items():
            
                if k[1] != 'line':
                    continue
                    
                if set([self.vertices[i], self.vertices[i - 1]]) == set(v):
                    self.unions += k[0] + ' U '
                    
        self.unions = self.unions[:-3]


    def find_location(self):

        x = int(self.center[0])
        y = int(self.center[1])

        if x == 50:
            self.hloc = 'center'
        elif x < 50:
            self.hloc = 'left'
        else:
            self.hloc = 'right'
        
        if y == 50:
            self.vloc = 'middle'
        elif y < 50:
            self.vloc = 'bottom'
        else:
            self.vloc = 'top'


    def store_crel(self, name, case):

        if case == 'i':
            self.crel.append('inside({},{})'.format(self.tag, name))
        elif case == 'o':
            self.crel.append('overlap({},{})'.format(self.tag, name))


    def store_hrel(self, name, case):

        if case == 'l':
            self.crel.append('left_of({},{})'.format(self.tag, name))
        elif case == 'r':
            self.crel.append('right_of({},{})'.format(self.tag, name))


    def store_vrel(self, name, case):

        if case == 'a':
            self.crel.append('above({},{})'.format(self.tag, name))
        elif case == 'b':
            self.crel.append('below({},{})'.format(self.tag, name))


    def print_relatives(self):
    
        for line in self.hrel:
            print(line)
            
        for line in self.vrel:
            print(line)
            
        for line in self.crel:
            print(line)


    def print_p(self):

        if self.unions != '':

            self.p_mid = '('

            for value in self.vertices:
                self.p_mid += '({}, {}),{}, '.format(value[0], value[1], Shape.k)

            self.p_mid = self.p_mid[:-4]
            self.p_mid += ')'

            self.p_line = self.tag + ' = scc' + self.p_mid + ' = ' + self.unions
            print(self.p_line)


    def print_shape(self):

        if not self.only_loop:
            self.s_line = self.kind + '(' + self.tag + ')'
            print(self.s_line)


    def print_pos(self):

        print('hloc(' + self.tag + ',' + self.hloc + ')')
        print('vloc(' + self.tag + ',' + self.vloc + ')')


    def get_p_line(self):

        if self.unions != '':

            self.p_mid = '('

            for value in self.vertices:
                self.p_mid += '({}, {}),{}, '.format(value[0], value[1], Shape.k)

            self.p_mid = self.p_mid[:-4]
            self.p_mid += ')'

            self.p_line = self.tag + ' = scc' + self.p_mid + ' = ' + self.unions
            return self.p_line


    def get_shape_line(self):

        if not self.only_loop:
            self.s_line = self.kind + '(' + self.tag + ')'
            return self.s_line


    def get_pos_lines(self):

        return 'hloc(' + self.tag + ',' + self.hloc + ')\nvloc(' + self.tag + ',' + self.vloc + ')'
