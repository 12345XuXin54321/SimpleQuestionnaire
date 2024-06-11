import remi.gui as gui
from remi import start, App
import base_gui


class ChoosePage(gui.VBox):
    def __init__(self, *args, **kwargs):
        super(ChoosePage, self).__init__(*args, **kwargs)

        self.style['justify-content'] = 'space-around'

        self.questionnaire_view = gui.Button(
            "创建和查看问卷", style='width: 160px; height: 90px')
        self.questionnaire_write = gui.Button(
            "填写问卷", style='width: 160px; height: 90px')
        self.append(self.questionnaire_view)
        self.append(self.questionnaire_write)

    def set_func(self, ques_view_func, ques_write_func):
        self.questionnaire_view.onclick.do(ques_view_func)
        self.questionnaire_write.onclick.do(ques_write_func)


class ReplyList(gui.VBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        title = gui.Label("回答列表")
        self.append(title)

        self.rep_list = []

    def add_rep(self, name):
        qi = base_gui.ChoosableItem()
        qi.set_data(name, self.on_rep_choose)
        self.rep_list.append(qi)
        self.append(qi)

    def on_rep_choose(self, weight: base_gui.ChoosableItem):
        print(weight.name.text)


class ViewReplyPage(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = ''

        self.ques_naire_list = ReplyList()
        for i in range(5):
            self.ques_naire_list.add_rep("name: " + str(i))
        self.add_item(self.ques_naire_list)

    def set_user(self, usr):
        self.user = usr

    def on_create_ques(self, weight):
        pass


class QuestionnaireList(gui.VBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.append(gui.Label("问卷列表"))

        self.ques_list = []

    def add_ques(self, name):
        qi = base_gui.ChoosableItem()
        qi.set_data(name, self.on_ques_choose)
        self.ques_list.append(qi)
        self.append(qi)

    def on_ques_choose(self, weight: base_gui.ChoosableItem):
        print("c1 ", weight.name.text)
        self.choose_func(weight)

    def set_choose_func(self, func):
        self.choose_func = func


class ViewQuestionnairePage(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = ''

        self.ques_naire_list = QuestionnaireList()
        self.ques_naire_list.set_choose_func(self.on_view_ques)
        for i in range(5):
            self.ques_naire_list.add_ques("name: " + str(i))
        self.add_item(self.ques_naire_list)

        self.create_ques = gui.Button("创建问卷")
        self.create_ques.onclick.do(self.on_create_ques)
        self.add_item(self.create_ques)

    def set_user(self, usr):
        self.user = usr

    def on_view_ques(self, w):
        print("c1 ", w.name.text)
        rp = ViewReplyPage(self)
        self.open_weight(rp)

    def on_create_ques(self, w):
        print("create")


class LoginPage(gui.HBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_name = gui.TextInput()
        self.login = gui.Button("登录或注册", style='width: 160px')
        self.login.onclick.do(self.on_login)

        self.append(self.user_name)
        self.append(self.login)

    def on_login(self, weight):
        if (self.user_name.text != ""):
            # self.notification_message(self.user_name.text + "登录成功")
            print(self.user_name.text)


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        self.container = base_gui.BaseWindowVBox()

        self.login_data = LoginPage()
        self.container.add_permanent_item(self.login_data)

        self.choose_page = ChoosePage(height=400)
        self.choose_page.set_func(self.view_ques_fn, self.write_ques_fn)
        self.container.add_item(self.choose_page)

        self.view_ques_page = ViewQuestionnairePage(self.container)

        return self.container

    def view_ques_fn(self, weight):
        self.container.open_weight(self.view_ques_page)

    def write_ques_fn(self, weight):
        self.container.remove_child(self.choose_page)
        print("bbb")


def run_webui():
    # start(MyApp, address='0.0.0.0', port=10001, multiple_instance=True)
    start(MyApp, address='0.0.0.0', port=10001)


run_webui()
