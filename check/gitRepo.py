import shutil

from git import Repo
from dotenv import load_dotenv
import os

from pathlib import Path

import datetime

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO = os.getenv('REPO')
IS_DEBUG = bool(int(os.getenv('DEBUG_MODE')))



if os.path.exists("./repo/.git"):
    repo = Repo("./repo/")
else:
    repo = Repo.clone_from(
        "https://mrm:{TOKEN_GITHUB}@github.com/{REPO}".format(TOKEN_GITHUB=GITHUB_TOKEN, REPO=REPO), "./repo")

with repo.config_reader() as git_config:
    try:
        mainGitEmail = git_config.get_value('user', 'email')
        mainGitUser = git_config.get_value('user', 'name')
    except:
        mainGitEmail = "None"
        mainGitUser = "None"


def changeGitUserToBot():
    with repo.config_writer() as gitConfig:
        gitConfig.set_value('user', 'email', 'bot@auto.com')
        gitConfig.set_value('user', 'name', 'Bot-auto')



def resetGitUser():
    global mainGitUser, mainGitEmail
    with repo.config_writer() as gitCnf:
        gitCnf.set_value('user', 'email', mainGitEmail)
        gitCnf.set_value('user', 'name', mainGitUser)

def getLatestRowProxies(num_n):
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "checkout", "remotes/origin/master", "collected-proxies"])
        shutil.copytree("./repo/collected-proxies/row-url", "collected-proxies/row-url", dirs_exist_ok=True)
        all_path = "collected-proxies/row-url/all_" + num_n
        active_path = "collected-proxies/row-url/actives_" + num_n
        shutil.copy("./repo/" + all_path, all_path)
        shutil.copy("./repo/" + active_path, active_path)

def getLatestActiveConfigs(num_n):
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "checkout", "remotes/origin/master", "collected-proxies"])
        shutil.copytree("./repo/collected-proxies/xray-json", "collected-proxies/xray-json", dirs_exist_ok=True)
        active_configs_path = "collected-proxies/xray-json/actives_now_" + num_n
        shutil.copy("./repo/" +active_configs_path, active_configs_path)
        # shutil.copy("./repo/collected-proxies/clash-meta", "collected-proxies/clash-meta", dirs_exist_ok=True)


def commitPushRowProxiesFile(num_n):
    if not IS_DEBUG:
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M %Z')
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "reset", "--hard", "origin/master"])
        repo.git.execute(["git", "pull"])
        shutil.copytree("collected-proxies/row-url", "./repo/collected-proxies/row-url", dirs_exist_ok=True)
        all_path = "collected-proxies/row-url/all_" + num_n
        active_path = "collected-proxies/row-url/actives_" + num_n
        shutil.copy(all_path, "./repo/" + all_path)
        shutil.copy(active_path, "./repo/" + active_path)
        repo.index.add(Path(all_path))
        repo.index.add(Path(active_path))
        #changeGitUserToBot()
        repo.index.commit('节点清理完成' + formatted_time)
        remote = repo.remote()
  #      remote.push('master')
        #resetGitUser()
  #      print('节点清理完成' + formatted_time)


def commitPushRActiveProxiesFile(num_n):
    if not IS_DEBUG:
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M %Z')
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "reset", "--hard", "origin/master"])
        repo.git.execute(["git", "pull"])
        shutil.copytree("collected-proxies/xray-json", "./repo/collected-proxies/xray-json", dirs_exist_ok=True)
        xray_path = "collected-proxies/xray-json/actives_now_" + num_n
        shutil.copy(xray_path, "./repo/" + xray_path)
  #      shutil.copytree("collected-proxies/clash-meta", "./repo/collected-proxies/clash-meta", dirs_exist_ok=True)
  #      repo.index.add([r'collected-proxies/clash-meta/*'])
        repo.index.add(Path(xray_path))
        #changeGitUserToBot()
        repo.index.commit('节点检查完成' + formatted_time)
        remote = repo.remote()
  #      remote.push('master')
        #resetGitUser()
  #      print('节点检查完成' + formatted_time)


def getLatestRowProxies_all():
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "checkout", "remotes/origin/master", "collected-proxies"])
        shutil.copytree("./repo/collected-proxies/row-url", "collected-proxies/row-url", dirs_exist_ok=True)
        all_path = "collected-proxies/row-url/all.txt"
        active_path = "collected-proxies/row-url/actives.txt"
        shutil.copy("./repo/" + all_path, all_path)
        shutil.copy("./repo/" + active_path, active_path)

def getLatestActiveConfigs_all():
    if not IS_DEBUG:
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "checkout", "remotes/origin/master", "collected-proxies"])
        shutil.copytree("./repo/collected-proxies/xray-json", "collected-proxies/xray-json", dirs_exist_ok=True)
        active_configs_path = "collected-proxies/xray-json/actives_all.txt"
        shutil.copy("./repo/" +active_configs_path, active_configs_path)
        # shutil.copy("./repo/collected-proxies/clash-meta", "collected-proxies/clash-meta", dirs_exist_ok=True)


def commitPushRowProxiesFile_all():
    if not IS_DEBUG:
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M %Z')
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "reset", "--hard", "origin/master"])
        repo.git.execute(["git", "pull"])
        shutil.copytree("collected-proxies/row-url", "./repo/collected-proxies/row-url", dirs_exist_ok=True)
        all_path = "collected-proxies/row-url/all.txt"
        active_path = "collected-proxies/row-url/actives.txt"
        shutil.copy(all_path, "./repo/" + all_path)
        shutil.copy(active_path, "./repo/" + active_path)
        repo.index.add(Path(all_path))
        repo.index.add(Path(active_path))
        #changeGitUserToBot()
        repo.index.commit('节点清理完成' + formatted_time)
        remote = repo.remote()
  #      remote.push('master')
        #resetGitUser()
  #      print('节点清理完成' + formatted_time)


def commitPushRActiveProxiesFile_all():
    if not IS_DEBUG:
        
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M %Z')
        repo.git.execute(["git", "fetch", "--all"])
        repo.git.execute(["git", "reset", "--hard", "origin/master"])
        repo.git.execute(["git", "pull"])
        shutil.copytree("collected-proxies/xray-json", "./repo/collected-proxies/xray-json", dirs_exist_ok=True)
        xray_path = "collected-proxies/xray-json/actives_all.txt"
        shutil.copy(xray_path, "./repo/" + xray_path)
  #      shutil.copytree("collected-proxies/clash-meta", "./repo/collected-proxies/clash-meta", dirs_exist_ok=True)
  #      repo.index.add([r'collected-proxies/clash-meta/*'])
        repo.index.add(Path(xray_path))
        #changeGitUserToBot()
        repo.index.commit('节点检查完成' + formatted_time)
        remote = repo.remote()
  #      remote.push('master')
        #resetGitUser()
  #      print('节点检查完成' + formatted_time)
