<template>
  <el-container class="layout">
    <el-header>
      <div class="header-content">
        <div class="logo" @click="$router.push('/')">电影平台</div>
        <el-menu mode="horizontal" :router="true" :default-active="$route.path">
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/community">原创社区</el-menu-item>
          <el-menu-item index="/video">视频</el-menu-item>
          <el-menu-item index="/visualization">数据可视化</el-menu-item>
        </el-menu>
        <div class="header-right">
          <el-input v-model="searchKeyword" placeholder="搜索电影..." style="width: 200px; margin-right: 15px;" @keyup.enter="search" />
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              {{ user?.username || '用户' }}
              <el-icon><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="favorites">我的收藏</el-dropdown-item>
                <el-dropdown-item v-if="user?.role === 'admin'" command="admin">管理后台</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const searchKeyword = ref('')

const user = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
})

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    router.push('/login')
    ElMessage.success('已退出登录')
  } else if (command === 'favorites') {
    router.push('/favorites')
  } else if (command === 'admin') {
    router.push('/admin')
  }
}

const search = () => {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/', query: { search: searchKeyword.value } })
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
}
.el-header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
}
.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}
.logo {
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
  cursor: pointer;
}
.el-menu {
  flex: 1;
  margin-left: 30px;
  border-bottom: none;
}
.header-right {
  display: flex;
  align-items: center;
}
.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
}
</style>