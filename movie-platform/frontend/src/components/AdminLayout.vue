<template>
  <el-container style="min-height: 100vh;">
    <el-aside width="200px" style="background-color: #304156;">
      <div class="logo" style="height: 60px; line-height: 60px; text-align: center; color: #fff; font-size: 18px; background-color: #1f2d3d;">
        管理后台
      </div>
      <el-menu :default-active="$route.path" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF">
        <el-menu-item index="/admin/movies">
          <el-icon><film /></el-icon>
          <span>电影管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/celebrities">
          <el-icon><user /></el-icon>
          <span>影人管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/users">
          <el-icon><user-filled /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background-color: #fff; border-bottom: 1px solid #e6e6e6; display: flex; align-items: center; justify-content: flex-end;">
        <el-button type="primary" link @click="$router.push('/')">返回首页</el-button>
        <span style="margin: 0 15px;">{{ user?.username }}</span>
        <el-button type="primary" link @click="logout">退出</el-button>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Film, User, UserFilled } from '@element-plus/icons-vue'

const router = useRouter()
const user = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
  router.push('/login')
  ElMessage.success('已退出登录')
}
</script>