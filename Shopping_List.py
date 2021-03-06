from kivymd.app import MDApp
from kivymd.uix.list import MDList, IconLeftWidget, IconRightWidget, OneLineIconListItem, \
    OneLineAvatarIconListItem, CheckboxRightWidget
from kivymd.icon_definitions import md_icons
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.toast import toast


class Textfield_Object(BoxLayout):
    my_textfield = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_textfield()

    def add_textfield(self):
        if not self.my_textfield:
            self.my_textfield = MDTextField()
            self.my_textfield.hint_text = "Enter new entry name:"
            self.my_textfield.multiline = False
            self.my_textfield.bind(on_text_validate=lambda x: MDApp.get_running_app().new_entry(obj=None))

        self.add_widget(self.my_textfield)


class ShoppingListApp(MDApp):

    def build(self):
        self.list_was_edited = False
        grid = GridLayout()
        grid.rows = 2
        screen = Screen()
        grid.add_widget(screen)
        scroll = ScrollView()
        bottom_nav = MDBottomNavigation(size_hint_y=.1)
        bottom_nav.add_widget(MDBottomNavigationItem(text="Sort List", icon='sort', on_tab_release=self.sort))
        bottom_nav.add_widget(
            MDBottomNavigationItem(text="Clear List", icon='delete-forever', on_tab_release=self.clear_list))

        grid.add_widget(bottom_nav)
        toolbar = MDToolbar(title="Shopping List", anchor_title="center")
        toolbar.left_action_items = [['plus', self.dialog_window]]
        toolbar.right_action_items = [['undo-variant', self.undo]]
        toolbar.elevation = 10
        screen.add_widget(scroll)
        self.kvmd_list = MDList()
        scroll.add_widget(self.kvmd_list)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = '400'
        self.kvmd_list.add_widget(toolbar)
        self.list_of_entries = []
        self.len_list_start = 0
        self.test_textfield = Textfield_Object()
        self.removed_item_list = []

        return grid

    def on_start(self):
        try:
            f = open("shopping_list.txt", "r")
            for x in f:
                self.entry_from_file(x[:-1])
            f.close()
            self.len_list_start = len(self.list_of_entries)

        except FileNotFoundError:
            f = open("shopping_list.txt", "x")
            f.close()

    def on_stop(self):
        self.save(obj=None)

    def sort(self, obj):
        dictionary_entries = {}

        for i in self.list_of_entries:
            dictionary_entries[i.text] = i
            self.kvmd_list.remove_widget(i)

        self.list_of_entries.clear()

        sorted_dict = sorted(dictionary_entries)

        for t in sorted_dict:
            self.kvmd_list.add_widget(dictionary_entries[t])
            self.list_of_entries.append(dictionary_entries[t])

        self.list_was_edited = True
        toast("List sorted.", .8)
        self.save(obj=None)

    def save(self, obj):
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

    def dialog_window(self, obj):
        self.dialog = MDDialog(
            title="Add new item:",
            size_hint=(0.9, 1),
            type="custom",
            content_cls=self.test_textfield,
            buttons=[
                MDFlatButton(
                    text="Add", on_release=self.new_entry
                ),
                MDFlatButton(
                    text="Cancel", on_release=lambda x: self.dialog.dismiss()
                ),

            ],

        )
        self.dialog.set_normal_height()
        self.dialog.open()
        self.dialog.bind(on_dismiss=lambda x: self.test_textfield.parent.remove_widget(self.test_textfield))
        # removes Textfield_Object instance from box_layout, otherwise it will try to add widget again to box_layout

    def new_entry(self, obj):
        new_name = self.test_textfield.my_textfield
        if new_name.text != '':
            icon_l = CheckboxRightWidget()
            icon_r = IconRightWidget(icon="close")
            self.new_item = OneLineAvatarIconListItem(text=new_name.text)
            self.new_item.add_widget(icon_l)
            self.new_item.add_widget(icon_r)
            self.kvmd_list.add_widget(self.new_item)
            self.list_of_entries.append(self.new_item)
            self.dialog.dismiss()
            icon_r.bind(on_release=self.remove_with_icon)
            new_name.text = ''
            self.save(obj=None)

        else:
            pass

    def remove_with_icon(self, obj):
        self.remove_entry(obj.parent.parent)

    def entry_from_file(self, name):
        icon_l = CheckboxRightWidget()
        icon_r = IconRightWidget(icon="close")
        self.new_item = OneLineAvatarIconListItem(text=name)
        self.new_item.add_widget(icon_l)
        self.new_item.add_widget(icon_r)
        self.kvmd_list.add_widget(self.new_item)
        self.list_of_entries.append(self.new_item)
        icon_r.bind(on_release=self.remove_with_icon)

    def remove_entry(self, obj):

        self.removed_item_list.append(obj)
        self.kvmd_list.remove_widget(obj)
        self.list_of_entries.remove(obj)
        self.list_was_edited = True
        self.save(obj=None)

    def clear_list(self, obj):
        toast('List was cleared.', .8)

        for i in self.list_of_entries:
            try:
                self.removed_item_list.append(i)
                self.kvmd_list.remove_widget(i)
            except AttributeError:
                pass
        self.list_of_entries.clear()
        self.list_was_edited = True
        self.save(obj=None)

    def undo(self, obj):
        try:
            self.kvmd_list.add_widget(self.removed_item_list[0])
            self.list_of_entries.append(self.removed_item_list[0])
            del self.removed_item_list[0]
            self.save(obj=None)
        except IndexError:
            pass

if __name__ == "__main__":
    app = ShoppingListApp()
    app.run()

