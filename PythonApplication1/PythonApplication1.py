# coding: UTF-8

"""
IDは1000番台はテキスト
    2000番台はボタン
"""
import pickle
import sys
import os
import wx
import wx.lib.agw.aui as aui
Projects = {}
projectName = ""
mode = 1
console_length = 80
proj_tab = {}

# 初期化処理
if not os.path.exists("Projects.txt"):          
    with open('Projects.txt', 'wb') as fout:
        pickle.dump(Projects, fout)
else:
    pass


class MainFrame(wx.Frame):
    """
    MainFrame class
    """

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,"BrainStorming",size=(800,600))
        
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self.notebook = aui.AuiNotebook(self, wx.ID_ANY,agwStyle=aui.AUI_NB_CLOSE_ON_ALL_TABS)
        

        self._mgr.AddPane(self.notebook, aui.AuiPaneInfo().Name("notebook_content").CenterPane().PaneBorder(False))
        self._mgr.Update()
        self.SetMenuBar(MainMenu())

        def selectMenu(event):
            if event.GetId() == 1001:
                create_project_frame = CreateProjectFrame()
                create_project_frame.Show()
            if event.GetId() == 1002:
                open_project = OpenProjectFrame(parent=self)
                open_project.Show()
            if event.GetId() == 1004:
                self.Close(True)

        
        self.Bind(wx.EVT_MENU,selectMenu)
    def addTab(self,string):
        proj_tab[string] = ProjectsTab(self.notebook)
        self.notebook.AddPage(proj_tab[string], string, False)
        self._mgr.Update()
class OpenProjectFrame(wx.Frame):

    def __init__(self,parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY,"aaaaaaa",size=(300,100))
        with open('Projects.txt', 'rb') as f:
            Projects = pickle.load((f))
        combobox_1 = wx.ComboBox(self, wx.ID_ANY, "SelectProject", choices=list(Projects.keys()),style=wx.CB_READONLY)
        open_project_button = wx.Button(self, 2001,"開く")
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(combobox_1, flag= wx.GROW)
        layout.Add(open_project_button, flag=wx.SHAPED | wx.ALIGN_RIGHT | wx.ALL, border=5)
        
        self.SetSizer(layout)
        

        def click_button(event):
            if event.GetId() == 2001:
                if len(combobox_1.GetValue()) > 0:
                    parent.addTab(combobox_1.GetValue())
                    self.Close(True)
        self.Bind(wx.EVT_BUTTON, click_button, open_project_button)

class CreateProjectFrame(wx.Frame):
    """
    CreateProjectFrame class
    """
    
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,"ProjectName",size=(300,100))
        with open('Projects.txt', 'rb') as f:
            Projects = pickle.load((f))
        #create_project_panel = wx.Panel(self, wx.ID_ANY)
        create_project_text = wx.TextCtrl(self, wx.ID_ANY)
        create_project_text.SetMaxLength(20)
        create_project_button = wx.Button(self, 2001,"作成")

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(create_project_text, flag=wx.EXPAND | wx.ALL, border = 5)
        layout.Add(create_project_button, flag=wx.SHAPED | wx.ALIGN_RIGHT | wx.ALL, border=5)
        self.SetSizer(layout)
        def add_proj(project):

            Projects[project] = {}
            with open('Projects.txt', 'wb') as f:
                pickle.dump(Projects, f)
            """with open('Projects.txt', 'rb') as f:
                Projects = pickle.load((f))"""
         
        def click_button(event):
            if event.GetId() == 2001:
                if len(create_project_text.GetValue()) > 0:
                    add_proj(create_project_text.GetValue())
                    self.Close(True)
        self.Bind(wx.EVT_BUTTON, click_button, create_project_button)

class ProjectsTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

class MainMenu(wx.MenuBar):

    def __init__(self):

        wx.MenuBar.__init__(self)

        menu_file = wx.Menu()
        create_project = menu_file.Append(1001, "新規プロジェクトを作成")
        open_project = menu_file.Append(1002, "プロジェクトを開く")
        save_project = menu_file.Append(1003,"保存")
        exit_bs = menu_file.Append(1004, "終了")

        self.Append(menu_file, "ファイル")
            
app = wx.App()
mainFrame = MainFrame()
mainFrame.Show()
app.MainLoop()


# プロジェクトやアイデアの中身を表示する
def display(dictionary):
    print("-" * console_length)
    if mode == 1:
        print("Projects")
    elif mode == 2:
        print("Project : " + projectName)
        print("Idea:")
    else:
        pass
    Project_OR_Idea_keys = list(dictionary.keys())
    Project_OR_Idea_keys.sort()
    for key in Project_OR_Idea_keys:
        print("・" + key)
    print("-" * console_length)

# プロジェクトを作成
def add_proj(project):
    Projects[project] = {}
    with open('Projects.txt', 'wb') as f:
        pickle.dump(Projects, f)
# プロジェクトを削除
def del_proj(projects):
    for project in projects:
        if project in Projects:
            del Projects[project]
            print(project + "を削除しました.")
            with open('Projects.txt', 'wb') as f:
                pickle.dump(Projects, f)
        else:
            print(project + "が見つかりませんでした.")
            continue

# プロジェクトの中身を表示
def project(projname):
    if projname in list(Projects.keys()):
        global projectName
        projectName = projname
    else:
        print("naiyo")

# アイデアを追加
def add_idea(project,title,idea):  
    Projects[project][title] = idea
    with open('Projects.txt', 'wb') as f:
        pickle.dump(Projects, f)

# アイデアを削除する
def del_idea(project,titles):
    for title in titles:
        if title in Projects[project]:
            del Projects[project][title]
            print(title + "を削除しました.")
            with open('Projects.txt', 'wb') as f:
                pickle.dump(Projects, f)
        else:
            print(title + "が見つかりませんでした.")
            continue

# アイデアの中身を表示
def idea(project,title):
    if title in Projects[project]:
        print(Projects[project][title])
    else:
        print(title + "が見つかりませんでした.")

# アイデアを文字の一致で検索
def find(project,word):
    for title in list(Projects[project].keys()):
        if word in title:
            print(title)
        else:
            continue
# 最初に戻る
def back():
    global projectName
    projectName = ""
# 様々なコマンドをまとめている
def commands(command):
    print("-" * console_length)
    if command == "quit":
        sys.exit()
    
    if mode == 1:
        if command == "add_proj":
            add_proj(input("ProjectName:"))
        elif command == "del_proj":
            del_proj(input("ProjectsName:").split())
        elif command == "project":
            project(input("ProjectName:"))
        else:
            print("コマンドが正しくありません.")

    elif mode == 2:
        if command == "add_idea":
            title1 = input("Title:")
            print("Idea:")
            add_idea(projectName,title1,sys.stdin.read())
        elif command == "del_idea":
            del_idea(projectName,input("Titles:").split())
        elif command == "idea":
            idea(projectName,input("Title:"))
        elif command == "find":
            find(projectName,input("word:"))
        elif command == "back":
            back()
        else:
            print("コマンドが正しくありません.")
# メイン
while (1):
    with open('Projects.txt', 'rb') as f:
        Projects = pickle.load((f))
    if projectName == "":
        mode = 1
        object = Projects
    else:
        mode = 2
        object = Projects[projectName]
    display(object)
    print("コマンドを入力してください:")
    commands(input())