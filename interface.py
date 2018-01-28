from tkinter import *
from tkinter.ttk import Combobox
from brand import Emulsion0
from mytk3 import ListWall


class Interface:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("%dx%d%+d%+d" % (600, 400, 0, 0))
        self.fr = None

        self.bot_frame = Frame(self.root, bg='yellow')
        self.bot_frame.pack(side=BOTTOM, fill=X)
        self.buttons = []

        self.to_choose_product()

    def mainloop(self):
        self.root.mainloop()

    def test(self, *args, **kwargs):
        self.fr = ChooseProduct(self.root)
        self.fr.pack(expand=YES, fill=BOTH)

    def fr_forget(self):
        if self.fr is not None:
            self.fr.pack_forget()
        for b in self.buttons:
            b.pack_forget()
        self.buttons = []

    def to_choose_product(self):
        self.fr_forget()

        self.fr = ChooseProduct(self.root, bg='yellow')
        self.fr.pack(expand=YES, fill=BOTH)

        self.buttons.append(Button(self.bot_frame,
                                   text='Next >',
                                   width=10,
                                   command=self.to_choose_batch_from_ch_prod))
        self.buttons[0].pack(side=RIGHT)

    def to_choose_bath(self, klass):
        self.fr_forget()

        self.fr = ChooseBatch(self.root, klass=klass)
        self.fr.pack(expand=YES, fill=BOTH)
        self.buttons.append(Button(self.bot_frame,
                                   text='Add >',
                                   width=10,
                                   command=self.to_add_product))
        self.buttons.append(Button(self.bot_frame,
                                   text='Certificate >'))
        self.buttons.append(Button(self.bot_frame,
                                   text='Edit >',
                                   width=10,
                                   command=self.to_edit))
        self.buttons.append(Button(self.bot_frame,
                                   text="delete",
                                   width=10,
                                   command=self.fr.delete_batch))
        self.buttons.append(Button(self.bot_frame,
                                   text='< Back',
                                   width=10,
                                   command=self.to_choose_product))
        self.buttons[-1].pack(side=LEFT)
        for b in self.buttons[:-1]:
            b.pack(side=RIGHT)

    def to_choose_batch_from_ch_prod(self):
        klass = self.fr.get()
        if not klass:
            return None
        else:
            self.to_choose_bath(klass)

    def to_choose_batch_from_input(self):
        klass = self.fr.product.__class__(is_empty=True)
        self.to_choose_bath(klass)

    def to_add_product(self):
        prod = self.fr.klass

        self.fr_forget()

        self.fr = InputBatch(self.root, product=prod)
        self.fr.pack(expand=YES, fill=BOTH)

        self.buttons.append(Button(self.bot_frame,
                                   text='Save',
                                   width=10,
                                   command=self.fr.save))
        self.buttons.append(Button(self.bot_frame,
                                   text='< Back',
                                   width=10,
                                   command=self.to_choose_batch_from_input))
        self.buttons[0].pack(side=RIGHT)
        self.buttons[1].pack(side=LEFT)

    def to_edit(self):
        prod = self.fr.get_batch()
        if prod is None:
            return None
        self.fr_forget()
        self.fr = InputBatch(self.root, prod)
        self.fr.pack(expand=YES, fill=BOTH)

        self.buttons.append(Button(self.bot_frame,
                                   text='< Back',
                                   width=10,
                                   command=self.to_choose_batch_from_input))
        self.buttons[0].pack(side=LEFT)


class ChooseProduct(Frame):
    brands = [Emulsion0,
              ]

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.config(bg='green', bd=1, relief=RAISED)
        self.center_frame = Frame(self, bg='red')
        self.center_frame.pack(anchor=CENTER, expand=YES)
        self.lab = Label(self.center_frame, text='Choose product:')
        self.lab.pack()
        self.cbb = Combobox(master=self.center_frame, values=[b.name for b in ChooseProduct.brands])
        self.cbb.pack()

    def get(self):
        brand = self.cbb.get()
        if not brand:
            return None
        for prod in self.brands:
            if prod.name == brand:
                return prod
        raise Exception('product not founded')


class Klass:
    def get_batches(self):
        return [(j, "{}, {}/10/2017".format(j + 10, j + 2)) for j in range(20)]


class ChooseBatch(Frame):
    def __init__(self, master, **kwargs):
        self.klass = kwargs.pop('klass')(is_empty=True)
        Frame.__init__(self, master, **kwargs)
        self.config(bg='green', bd=1, relief=RAISED)
        #self.klass = kwargs['klass']
        #self.klass = Klass()
        options = self.batch_processing()
        self.lst = ListWall(self, options=options)
        self.lst.lst.config(width=60)
        self.lst.pack()
        
    def batch_processing(self):
        batchs = self.klass.get_batches()
        if batchs:
            patt = '{}, {}'
            options = []
            for batch in batchs:
                bd = self.klass.get_batch_date(batch)
                options.append(patt.format(batch, bd))
        else:
            options = ['Where is\'t any batches :(']
        return options
            
    def get_select(self):
        """
        foo - list, contains selected element of Listbox or nothing,
        if nothing selected. If foo is empty, the function does nothing visually.
        bar - selected element. it is string, contains batch number and date separated by ','
        or batch abscence message.
        determination of baz is trying to find separator and determinate what is bar.
        if bar is batch abscence message than the function does nothing visually.
        else the function return batch number (baz[0]).
        """
        foo = self.lst.get(self.lst.curselection())
        if not foo:
            print('path 1')
            return None
        bar = foo[0]
        try:
            baz = int(bar.split(', ')[0])
        except ValueError:
            print('path 2')
            return None
        else:
            print('path 3')
            return str(baz)
            
    def get_batch(self):
        batch = self.get_select()
        if batch is None:
            return None
        else:
            d = self.klass.get_obj_from_store(batch)
            return self.klass(**d)

    def delete_batch(self):
        print('del')
        batch = self.get_select()
        print(batch)
        if batch is None:
            return None
        else:
            self.klass.rm(batch)
            self.lst.clear()
            self.lst.makelist(options=self.batch_processing())


class InputBatch(Frame):
    properties = [('date', ''),
                  ('batch', ''),
                  ('appearance', ''),
                  ('nvc', ''),
                  ('vms', ''),
                  ('vz4', ''),
                  ('vz6', ''),
                  ('brookf', ''),
                  ('ph', ''),
                  ('dens', ''),
                  ('gluing_paper', ''),
                  ('gluing_cardboard', ''),
                  ('drying_cardboard', ''),
                  ('vz4_1_3', ''),
                  ('bubbling_vol_1_3', ''),
                  ('bubbling_time_1_3', ''),
                  ('vz4_1_5', ''),
                  ('thermastab', '')]

    def __init__(self, master, product, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.config(bg='blue')
        self.lines = {}
        self.product = product

        for prop in self.properties:
            # prop[0] is the attribute name
            # adding is the attribute value
            if hasattr(product, prop[0]):
                if not product.is_empty:
                    # adding must be tuple to concatenate with prop
                    adding = (getattr(product, prop[0]),)
                else:
                    adding = ()
                self.lines[prop[0]] = Line(self)
                self.lines[prop[0]].set_name(prop + adding)
                self.lines[prop[0]].pack(fill=X)
            else:
                print('has not attr {}'.format(prop[0]))

    def get_dict(self):
        ret = {}
        for key in self.lines.keys():
            ret[key] = self.lines[key].get_value()
        return ret

    def save(self):
        """
        create not empty product class based on this form
        and call its save method
        :return: None
        """
        obj = self.product(**self.get_dict())
        obj.save()


class Line(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.lab = Label(self, width=15, anchor=W)
        self.value = Label(self, width=10, anchor=CENTER)
        self.ent = Entry(self, width=10)
        self.name = ''

    def set_name(self, name):
        self.lab.config(text=(name[1] or name[0]))
        self.lab.pack(side=LEFT)
        if len(name) > 2:
            self.value.config(text=name[2])
            self.value.pack(side=LEFT)
        self.ent.pack(side=RIGHT)

    def get_name(self):
        return self.name

    def get_value(self):
        return self.ent.get()


class AddNewBatch(Frame):
    def __init__(self, master, product, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.product = product


if __name__ == '__main__':
    test = ['batch', 'date', 'ph', 'dens', 'visc_brookf', 'nvc', 'thermastab']
    inter = Interface()
    inter.mainloop()
