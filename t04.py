class animel():
    def __init__(self,name = '',ani = '',age = ''):
        self.name = name
        self.ani = ani
        self.age = age

    def __str__(self):
        return 'name:' + self.name+'\n' +'ani:' + self.ani +'\n' +'age:' +  str(self.age)

    def whoami(self):
        print(self.name)
   # def plus(self):
    #    self.age += 1
    def voice(self,another = ''):
        if self.ani =='dog':
            print('woooooo')
        elif self.ani =='cat':
            print('mewwwwww')
        else:
            print(another)

'''
def main():
    a = animel('qdd','dog',5)
    a.plus()
    #print(a.ani,a.age)
    print(a)
    a.whoami()
    a.voice()

if __name__ == '__main__':
    main()
'''
class animal2(animel):
    def __init__(self, name='', ani='', age='',color = ''):
        self.color = color
        super(animal2,self).__init__(name,ani,age)
    def __str__(self):
        return 'name:' + self.name+'\n' +'ani:' + self.ani +'\n' +'age:' +  str(self.age)+'\n'+'color:' + self.color
    def qoo(self):
        print('qoo')
    def whoami(self):
        print('')
        super(animal2, self).whoami()
        print('')
        


b = animal2('qdd2', 'cat',8,'yellow')

# print(a.ani,a.age)
print(b)
print(b.color)
b.whoami()
b.voice()
b.qoo()

