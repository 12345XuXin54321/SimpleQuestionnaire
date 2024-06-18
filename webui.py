import remi.gui as gui
from remi import start, App
import base_gui
import datamanage

gl_data_manage = datamanage.DataManage()


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


class AnswerInfo(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self, respondents_ind):
        resp_list = gl_data_manage.get_data(
            "respondents_data_tab", "answer_ind, ind", "respondents_ind = " + str(respondents_ind))
        for i in resp_list:
            answer_ind, ind = i
            resp_content = gl_data_manage.get_data(
                "answer_tab", "content", "ind = " + str(answer_ind))
            resp_content = list(resp_content[0])[0]
            dli = gui.Label("第{}题的回答 ".format(ind) + resp_content)
            self.append(dli)


class QuestionnaireInfo(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self, naire_ind):
        prob_list = gl_data_manage.get_data(
            "questionnaire_data_tab", "ques_ind, ind", "naire_ind = " + str(naire_ind))
        for i in prob_list:
            ques_ind, ind = i
            ques_content = gl_data_manage.get_data(
                "question_tab", "content", "ind = " + str(ques_ind))
            ques_content = list(ques_content[0])[0]
            dli = gui.Label("第{}题 ".format(ind) + ques_content)
            self.append(dli)


class ReplyList(gui.VBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        title = gui.Label("回答列表")
        self.append(title)

        self.rep_list = []

    def add_rep(self, name, ind):
        qi = base_gui.ChoosableItem()
        qi.set_data(name, self.on_rep_choose, ind)
        self.rep_list.append(qi)
        self.append(qi)

    def set_choose_func(self, choose_func):
        self.choose_fn = choose_func

    def on_rep_choose(self, weight: base_gui.ChoosableItem):
        print(weight.name.text)
        self.choose_fn(weight)


class ViewReplyPage(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = ''

        view_ques = gui.Button("查看问题")
        view_ques.onclick.do(self.on_view_ques)
        self.add_item(view_ques)

        self.ques_naire_list = ReplyList()
        self.ques_naire_list.set_choose_func(self.on_view_ans)
        self.add_item(self.ques_naire_list)

    def update_data(self):
        res_list = gl_data_manage.get_data(
            "questionnaire_fillout_tab", "respondents_ind", "naire_ind = " + str(self.naire_ind))
        for i in res_list:
            resp_ind = list(i)[0]
            self.ques_naire_list.add_rep("name: " + str(resp_ind), resp_ind)

    def set_user(self, usr):
        self.user = usr

    def set_naire_ind(self, ind):
        self.naire_ind = ind

    def on_view_ans(self, weight):
        ai = AnswerInfo(self)
        ai.get_data(weight.other_data)
        self.open_weight(ai)

    def on_view_ques(self, w):
        qi = QuestionnaireInfo(self)
        qi.get_data(self.naire_ind)
        self.open_weight(qi)


class QuestionnaireList(gui.VBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.append(gui.Label("问卷列表"))

        self.ques_list = []

    def add_ques(self, name, ind):
        qi = base_gui.ChoosableItem()
        qi.set_data(name, self.on_ques_choose, ind)
        self.ques_list.append(qi)
        self.append(qi)

    def on_ques_choose(self, weight: base_gui.ChoosableItem):
        print("c1 ", weight.name.text)
        self.choose_func(weight)

    def set_choose_func(self, func):
        self.choose_func = func


class CreateQuestionnairePage(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        release_ques = gui.Button("发布问卷")
        release_ques.onclick.do(self.rele_ques_func)
        add_ques = gui.Button("添加问题")
        add_ques.onclick.do(self.add_ques_func)

        self.control_hbox = gui.HBox(style='width: 320px')
        self.control_hbox.append(add_ques)
        self.control_hbox.append(release_ques)
        self.control_hbox.style['justify-content'] = 'space-around'

        self.ques_input_list = []

        self.add_item(self.control_hbox)

    def add_ques_func(self, w):
        ques_input = gui.TextInput()
        self.ques_input_list.append(ques_input)
        self.append(ques_input)

    def set_userid(self, user_id):
        self.userid = user_id

    def rele_ques_func(self, w):
        ques_list = []
        for s in self.ques_input_list:
            ques_list.append(s.text)
        print(ques_list)

        ques_count = gl_data_manage.db_len("question_tab")
        questionnaire_count = gl_data_manage.db_len("questionnaire_tab")

        for i in range(len(ques_list)):
            gl_data_manage.insert_data(
                "question_tab", [i + ques_count, ques_list[i]])

        gl_data_manage.insert_data("questionnaire_tab", [
                                   questionnaire_count, "title_" + str(questionnaire_count)])

        for i in range(len(ques_list)):
            gl_data_manage.insert_data("questionnaire_data_tab", [
                                       i + ques_count, questionnaire_count, i])

        gl_data_manage.insert_data("create_questionnaire_tab", [
                                   self.userid, questionnaire_count])


class ViewQuestionnairePage(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = ''

    def update_data(self):
        self.ques_naire_list = QuestionnaireList()
        self.ques_naire_list.set_choose_func(self.on_view_ques)
        user_naires = gl_data_manage.get_data(
            "create_questionnaire_tab", "naire_ind", "user_ind = " + str(self.user))

        for naire_ind in user_naires:
            naire_ind = list(naire_ind)
            naire_ind = naire_ind[0]
            d_pk = gl_data_manage.get_data(
                "questionnaire_tab", "*", "ind = " + str(naire_ind))
            d_pk = list(d_pk[0])
            ind = d_pk[0]
            title = d_pk[1]

            self.ques_naire_list.add_ques(title, ind)
        self.add_item(self.ques_naire_list)

        self.create_ques = gui.Button("创建问卷")
        self.create_ques.onclick.do(self.on_create_ques)
        self.add_item(self.create_ques)

    def set_user(self, usr):
        self.user = usr

    def on_view_ques(self, w):
        print("c1 ", w.name.text)
        rp = ViewReplyPage(self)
        rp.set_user(self.user)
        rp.set_naire_ind(w.other_data)
        rp.update_data()
        self.open_weight(rp)

    def on_create_ques(self, w):
        cp = CreateQuestionnairePage(self)
        cp.set_userid(self.user)
        self.open_weight(cp)


class ReplyQuestionPage(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ok_button = gui.Button("确认提交")
        self.ok_button.onclick.do(self.submit_data)
        self.ans_text_list = []
        self.add_item(self.ok_button)

    def update_data(self, naire_ind, user_ind):
        self.user_id = user_ind
        self.naire_ind = naire_ind
        prob_list = gl_data_manage.get_data(
            "questionnaire_data_tab", "ques_ind", "naire_ind = " + str(naire_ind))
        prob_len = len(prob_list)

        for i in range(prob_len):
            hb = gui.HBox()

            prob_ind = list(prob_list[i])[0]
            prob_text = gl_data_manage.get_data(
                "question_tab", "content", "ind = " + str(prob_ind))
            prob_text = list(prob_text[0])[0]
            ques_lab = gui.Label("问题" + str(i) + " " + prob_text)
            text_input = gui.TextInput()
            self.ans_text_list.append(text_input)

            hb.append(ques_lab)
            hb.append(text_input)

            self.add_item(hb)

    def submit_data(self, w):
        ans_last = []
        for ti in self.ans_text_list:
            ans_last.append(ti.text)

        resp_ind = gl_data_manage.db_len("respondents_tab")
        ans_len = gl_data_manage.db_len("answer_tab")

        gl_data_manage.insert_data("reply_questionnaire_tab", [
                                   self.user_id, resp_ind])
        gl_data_manage.insert_data("respondents_tab", [resp_ind])
        gl_data_manage.insert_data("questionnaire_fillout_tab", [
                                   resp_ind, self.naire_ind])

        for i in range(len(ans_last)):
            gl_data_manage.insert_data(
                "answer_tab", [ans_len + i, ans_last[i]])
            gl_data_manage.insert_data("respondents_data_tab", [
                                       resp_ind, ans_len + i, i])


class FillOutQuestionnairePage(base_gui.WindowVBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        lab = gui.Label("填写问卷标识符")
        self.text_input = gui.TextInput()
        button = gui.Button("开始填写")
        button.onclick.do(self.onstartFIllOut)
        self.add_item(lab)
        self.add_item(self.text_input)
        self.add_item(button)

    def set_userid(self, userid):
        self.user_ind = userid

    def onstartFIllOut(self, w):
        rqp = ReplyQuestionPage(self)
        rqp.update_data(int(self.text_input.text), self.user_ind)
        self.open_weight(rqp)


class LoginPage(gui.HBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_name = gui.TextInput()
        self.login = gui.Button("登录或注册", style='width: 160px')
        self.login.onclick.do(self.on_login)
        self.now_status = gui.Label("未登录")

        self.append(self.user_name)
        self.append(self.login)
        self.append(self.now_status)

    def on_login(self, weight):
        if (self.user_name.text != ""):
            # self.notification_message(self.user_name.text + "登录成功")
            user_id = int(self.user_name.text)
            r_data = gl_data_manage.get_data(
                "users_tab", "*", "user_ind = " + str(user_id))
            login_status = ""

            if (len(r_data) == 0):
                print(user_id, "注册")
                gl_data_manage.insert_data(
                    "users_tab", [user_id, "user_name_" + str(user_id)])
                login_status = "user_name_" + str(user_id) + "注册成功"
            else:
                login_status = "user_name_" + str(user_id) + "已登录"

            r_data = gl_data_manage.get_data(
                "users_tab", "*", "user_ind = " + str(user_id))

            t_userid, t_username = r_data[0]
            self.now_status.set_text(login_status)
            print(t_userid, t_username, "登录成功")

    def get_userid(self):
        return int(self.user_name.text)


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        self.container = base_gui.BaseWindowVBox()

        self.login_data = LoginPage()
        self.container.add_item(self.login_data)

        self.choose_page = ChoosePage(height=400)
        self.choose_page.set_func(self.view_ques_fn, self.write_ques_fn)
        self.container.add_item(self.choose_page)

        return self.container

    def view_ques_fn(self, weight):
        vpq = ViewQuestionnairePage(self.container)
        vpq.set_user(self.login_data.get_userid())
        vpq.update_data()
        self.container.open_weight(vpq)

    def write_ques_fn(self, weight):
        foqp = FillOutQuestionnairePage(self.container)
        foqp.set_userid(self.login_data.get_userid())
        self.container.open_weight(foqp)


def run_webui():
    # start(MyApp, address='0.0.0.0', port=10001, multiple_instance=True)
    start(MyApp, address='0.0.0.0', port=10001)


run_webui()
