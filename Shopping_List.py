from kivymd.app import MDApp
from kivymd.uix.list import MDList, TwoLineIconListItem, OneLineListItem, OneLineAvatarIconListItem
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextFieldRect, MDTextField, MDTextFieldRound
from kivy.uix.scrollview import ScrollView
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
from kivy.lang import Builder
from kivymd.uix.list import IconLeftWidget, IconRightWidget, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons


class ShoppingListApp(MDApp):
    def build(self):
        self.list_was_edited = False
        screen = Screen()
        scroll = ScrollView()
        self.list_of_entries = []
        self.len_list_start = 0
        self.kvmd_list = MDList()
        self.theme_cls.theme_style = "Dark"
        screen.add_widget(scroll)
        scroll.add_widget(self.kvmd_list)
        add_entry = MDFlatButton(text="Zatwierdź", pos_hint={"center_x": .5, "center_y": .2},
                                 on_press=self.new_entry)
        screen.add_widget(add_entry)
        self.text_input = MDTextFieldRect(hint_text="Dodaj artykuł do listy", pos_hint={"center_x": .5, "center_y": .1},
                                          size_hint=(1, None), height="30dp", width="100dp", multiline=False,
                                          on_text_validate=self.new_entry)
        screen.add_widget(self.text_input)

        return screen

    def on_start(self):
        try:
            f = open("shopping_list.txt", "r")
            for x in f:
                self.list_of_entries.append(x[:-1])
                self.entry_from_file(x[:-1])
            f.close()
            self.len_list_start = len(self.list_of_entries)

        except:
            pass

    def on_stop(self):
        if self.list_was_edited is False:
            if self.len_list_start != len(self.list_of_entries):
                f = open("shopping_list.txt", "w")

                for i in self.list_of_entries:
                    if type(i) is str:
                        pass
                    elif type(i) is not str:
                        f.write(str(i.text) + "\n")
                f.close()
            else:
                pass
        elif self.list_was_edited is True:
            f = open("shopping_list.txt", "w")

            for i in self.list_of_entries:
                if type(i) is str:
                    pass
                elif type(i) is not str:
                    f.write(i.text + "\n")

            f.close()

    def new_entry(self, obj):
        if self.text_input.text != '':
            new_name = self.entry_name()
            icon_l = IconLeftWidget(icon="shopping")
            self.new_item = OneLineIconListItem(text=new_name)
            self.new_item.add_widget(icon_l)
            self.kvmd_list.add_widget(self.new_item)
            self.list_of_entries.append(self.new_item)
            self.new_item.bind(on_press=self.remove_entry)
            self.text_input.text = ''
        else:
            pass

    def entry_from_file(self, name):
        icon_l = IconLeftWidget(icon="shopping")
        self.new_item = OneLineIconListItem(text=name)
        self.new_item.add_widget(icon_l)
        self.kvmd_list.add_widget(self.new_item)
        self.list_of_entries.append(self.new_item)
        self.new_item.bind(on_press=self.remove_entry)
        self.text_input.text = ''

    def entry_name(self):
        name = self.text_input.text
        return name

    def remove_entry(self, obj):
        self.kvmd_list.remove_widget(obj)
        self.list_of_entries.remove(obj)
        self.list_was_edited = True


ShoppingListApp().run()
