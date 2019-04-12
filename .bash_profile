# terminal colors
export TERM="xterm-color"
PS1='\[\e[0;33m\]\u\[\e[0m\]@\[\e[0;32m\]\h\[\e[0m\]:\[\e[0;34m\]\w\[\e[0m\]\$ '

# Tell ls to be colourful: https://apple.stackexchange.com/questions/33677/how-can-i-configure-mac-terminal-to-have-color-ls-output
export CLICOLOR=1
export LSCOLORS=Exfxcxdxbxegedabagacad

# Tell grep to highlight matches
export GREP_OPTIONS='--color=auto'

export PATH="$PATH:/usr/local/sbin"

# maven
export MAVEN_HOME="/Users/leon/devtools/maven353"
export PATH="$MAVEN_HOME/bin:$PATH"

# pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

# redis
export PATH="/Users/leon/devtools/redis-4.0.9/src:$PATH"

# protoc protobuf
# export PATH="/usr/local/protobuf/bin:$PATH"

if which pyenv > /dev/null;
  then eval "$(pyenv init -)";
fi

# pyenv-virtualenv
if which pyenv-virtualenv-init > /dev/null;
  then eval "$(pyenv virtualenv-init -)";
fi

# python3
export PATH="/usr/local/Cellar/python/3.7.3/bin:$PATH"

alias ll='ls -al'

#cmd line style
## Parses out the branch name from .git/HEAD:
find_git_branch () {
  local dir=. head
  until [ "$dir" -ef / ]; do
    if [ -f "$dir/.git/HEAD" ]; then
      head=$(< "$dir/.git/HEAD")
      if [[ $head = ref:\ refs/heads/* ]]; then
        git_branch=" → ${head#*/*/}"
      elif [[ $head != '' ]]; then
        git_branch=" → (detached)"
      else
        git_branch=" → (unknow)"
      fi
      return
    fi
    dir="../$dir"
  done
  git_branch=''
}

PROMPT_COMMAND="find_git_branch; $PROMPT_COMMAND"
# Heree
black=$'\[\e[1;30m\]'
red=$'\[\e[1;31m\]'
green=$'\[\e[1;32m\]'
yellow=$'\[\e[0;33m\]'
blue=$'\[\e[1;34m\]'
magenta=$'\[\e[0;35m\]'
cyan=$'\[\e[0;34m\]'
white=$'\[\e[1;37m\]'
normal=$'\[\e[m\]'
#PS1="$white[$magenta\u$white@$green\h$white:$cyan\w$yellow\$git_branch$white]\$ $normal"
PS1="$magenta\u$white:$cyan\w$yellow\$git_branch]\[\e[0m\]\$ $normal"
#####

#git auto complete
source "/Users/leon/.git-completion"
alias em='/usr/local/Cellar/emacs/26.1_1/bin/emacs'
alias bxl='cd ~/go/src/github.com/borderxlab'
alias now='date "+%Y-%m-%d %H:%M:%S %a %Z"'
alias nows='date +%s'
#alias redis-server='cd /Users/leon/devtools/redis-4.0.9/src && ./redis-server && cd -'
#alias redis-cli='cd /Users/leon/devtools/redis-4.0.9/src && ./redis-cli && cd -'
alias datapipe='cd /Users/leon/codes/inventory-data-pipeline/Scrapy/prod_crawl/'
alias refresh='source ~/.bash_profile && date "+%Y-%m-%d %H:%M:%S"'
alias cmdline='ln -s /Users/leon/.pyenv/versions/2.7.14/lib/python2.7/site-packages/scrapy/cmdline.py'
alias session='cp ~/session* .'
alias goget='go get'
alias bulldozer='cd ~/go/src/GoEclipseSpace/bulldozer/src && rm -rf main && ln -s ~/codes/inventory-data-pipeline/bulldozer/src/main'
alias gitchk='git stash && git pull && git stash pop'
alias py='python'
alias gp='git pull'
alias gpp='git pull --rebase && git push'
alias prodpg='ssh -N -L 3433:rdszvm7r0p025c31nz2b593.pg.rds.aliyuncs.com:3433 api-prod1v'
alias devpg='ssh -N -L 3444:rdsf151i31dap967n2tw.pg.rds.aliyuncs.com:3433 api-dev'
alias prodes='ssh -N -L 9200:localhost:9200 -L 9000:localhost:9000 es1'
alias devcatalog='ssh -N -L 9000:localhost:9000 -L 9200:localhost:9250 -L 9300:localhost:9300 -L 8083:47.88.55.150:8083 api-dev'
alias deves='ssh -N -L 9250:localhost:9250 api-dev'
alias devestcp='ssh -N -L 9300:localhost:9300 api-dev'
alias catalog='cd /Users/leon/go/src/GoEclipseSpace/product-search/api'
alias gobxl='cd ~/go/src/github.com/borderxlab'
alias usd='http https://5thave-prod.bieyangapp.com/api/v1/_internal/exchangerate'
alias invmeta='python /Users/leon/eclipse-workspace/MyLab/inv_meta_dict.py >/dev/null 2>&1 &'
alias dpredis='ssh -N -L 6379:10.0.0.24:6379 datapipe1'
alias esstatus='curl localhost:9250/_cat/indices | grep open && curl localhost:9250/_cat/aliases'
alias fpath='find $PWD -maxdepth 1 -name '
alias datapiperedis='ssh -N -L 6379:10.0.0.24:6379 realtime1'
alias cpbytool='cp ~/codes/inventory-data-pipeline/Scrapy/prod_crawl/tools/bieyang.html ~/eclipse-workspace/MyLab/tools/'
alias gopull='go run pull.go --5thave 5thave-prod.bybieyang.com'
alias showhide='defaults write com.apple.finder AppleShowAllFiles TRUE'

# GOlang paths
export GOROOT=/usr/local/Cellar/go/1.10.2/libexec
export GOOS=darwin
export GOPATH=/Users/leon/go

export PRODUCT_SEARCH_CODEBASE=/Users/leon/go/src/GoEclipseSpace/product-search
export ES_BIN=/Users/leon/devtools/elasticsearch-5.5.3/bin/elasticsearch
