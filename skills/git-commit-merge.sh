#!/bin/bash

# Git 提交并合并到主分支脚本
# 用途：在当前分支提交更改，推送到远程，合并到 main 分支，然后切回当前分支

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取当前分支名
CURRENT_BRANCH=$(git branch --show-current)

echo -e "${BLUE}=== Git 提交并合并流程 ===${NC}"
echo -e "${YELLOW}当前分支: ${CURRENT_BRANCH}${NC}"

# 检查是否在 main 分支
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo -e "${RED}错误: 当前已在 main 分支，请切换到开发分支后再执行${NC}"
    exit 1
fi

# 检查是否有未提交的更改
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}没有需要提交的更改${NC}"
else
    # 显示当前状态
    echo -e "\n${BLUE}当前更改:${NC}"
    git status --short
    
    # 提示输入提交信息
    echo -e "\n${YELLOW}请输入提交信息 (留空使用默认信息):${NC}"
    read -r COMMIT_MSG
    
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="更新代码"
    fi
    
    # 添加所有更改
    echo -e "\n${BLUE}1. 添加所有更改...${NC}"
    git add .
    
    # 提交更改
    echo -e "${BLUE}2. 提交更改...${NC}"
    git commit -m "$COMMIT_MSG"
    echo -e "${GREEN}✓ 提交成功${NC}"
fi

# 推送到远程当前分支
echo -e "\n${BLUE}3. 推送到远程 ${CURRENT_BRANCH} 分支...${NC}"
git push origin "$CURRENT_BRANCH"
echo -e "${GREEN}✓ 推送成功${NC}"

# 切换到 main 分支
echo -e "\n${BLUE}4. 切换到 main 分支...${NC}"
git checkout main
echo -e "${GREEN}✓ 已切换到 main 分支${NC}"

# 拉取最新的 main 分支
echo -e "\n${BLUE}5. 拉取最新的 main 分支...${NC}"
git pull origin main
echo -e "${GREEN}✓ 拉取成功${NC}"

# 合并开发分支到 main
echo -e "\n${BLUE}6. 合并 ${CURRENT_BRANCH} 到 main...${NC}"
if git merge "$CURRENT_BRANCH" --no-edit; then
    echo -e "${GREEN}✓ 合并成功${NC}"
else
    echo -e "${RED}✗ 合并失败，请手动解决冲突${NC}"
    exit 1
fi

# 推送 main 分支到远程
echo -e "\n${BLUE}7. 推送 main 分支到远程...${NC}"
git push origin main
echo -e "${GREEN}✓ 推送成功${NC}"

# 切回原分支
echo -e "\n${BLUE}8. 切回 ${CURRENT_BRANCH} 分支...${NC}"
git checkout "$CURRENT_BRANCH"
echo -e "${GREEN}✓ 已切回 ${CURRENT_BRANCH} 分支${NC}"

echo -e "\n${GREEN}=== 所有操作完成！===${NC}"
echo -e "${BLUE}当前分支: $(git branch --show-current)${NC}"
