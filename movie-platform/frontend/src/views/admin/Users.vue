<template>
  <div class="admin-users">
    <h2>用户管理</h2>
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-input v-model="searchForm.username" placeholder="用户名" clearable @clear="fetchData" @keyup.enter="fetchData" />
      </el-col>
      <el-col :span="6">
        <el-input v-model="searchForm.email" placeholder="邮箱" clearable @clear="fetchData" @keyup.enter="fetchData" />
      </el-col>
      <el-col :span="4">
        <el-button type="primary" @click="fetchData">查询</el-button>
      </el-col>
    </el-row>

    <el-table :data="users" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="gender" label="性别" width="60" />
      <el-table-column prop="age" label="年龄" width="60" />
      <el-table-column prop="region" label="地区" />
      <el-table-column label="角色" width="150">
        <template #default="{ row }">
          <el-tag v-for="role in row.roles" :key="role.id" size="small" style="margin-right: 3px;">{{ role.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">{{ row.is_active ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template #default="{ row }">
          <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
          <el-button size="small" :type="row.is_active ? 'warning' : 'success'" @click="toggleActive(row)">
            {{ row.is_active ? '禁用' : '启用' }}
          </el-button>
          <el-button size="small" type="primary" @click="openRoleDialog(row)">分配角色</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="page"
      v-model:page-size="perPage"
      :total="total"
      :page-sizes="[10, 20, 50]"
      layout="total, sizes, prev, pager, next"
      @size-change="fetchData"
      @current-change="fetchData"
      style="margin-top: 20px;"
    />

    <!-- 编辑用户信息对话框 -->
    <el-dialog title="编辑用户" v-model="editDialogVisible" width="500px">
      <el-form :model="editForm" ref="editFormRef" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="editForm.phone" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="editForm.gender">
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input-number v-model="editForm.age" :min="0" :max="150" />
        </el-form-item>
        <el-form-item label="地区" prop="region">
          <el-input v-model="editForm.region" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEdit" :loading="editLoading">保存</el-button>
      </template>
    </el-dialog>

    <!-- 分配角色对话框 -->
    <el-dialog title="分配角色" v-model="roleDialogVisible" width="400px">
      <el-form>
        <el-form-item label="角色">
          <el-select v-model="selectedRoles" multiple placeholder="请选择角色">
            <el-option v-for="role in allRoles" :key="role.id" :label="role.name" :value="role.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRoles" :loading="roleLoading">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const users = ref([])
const total = ref(0)
const page = ref(1)
const perPage = ref(10)

const searchForm = reactive({
  username: '',
  email: ''
})

const fetchData = async () => {
  try {
    const params = {
      page: page.value,
      per_page: perPage.value,
      ...searchForm
    }
    if (!params.username) delete params.username
    if (!params.email) delete params.email
    const res = await request.get('/api/users/', { params })
    users.value = res.data
    total.value = res.total
  } catch (error) {
    console.error(error)
  }
}

// 编辑用户
const editDialogVisible = ref(false)
const editFormRef = ref(null)
const editLoading = ref(false)
const editForm = reactive({
  id: null,
  email: '',
  phone: '',
  gender: '',
  age: null,
  region: ''
})

const openEditDialog = (row) => {
  editForm.id = row.id
  editForm.email = row.email || ''
  editForm.phone = row.phone || ''
  editForm.gender = row.gender || ''
  editForm.age = row.age || null
  editForm.region = row.region || ''
  editDialogVisible.value = true
}

const saveEdit = async () => {
  editLoading.value = true
  try {
    await request.put(`/api/users/${editForm.id}`, editForm)
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error(error)
  } finally {
    editLoading.value = false
  }
}

// 启用/禁用
const toggleActive = async (row) => {
  try {
    await request.put(`/api/users/${row.id}/toggle-active`)
    row.is_active = !row.is_active
    ElMessage.success(row.is_active ? '已启用' : '已禁用')
  } catch (error) {
    console.error(error)
  }
}

// 分配角色
const roleDialogVisible = ref(false)
const roleLoading = ref(false)
const allRoles = ref([])
const selectedRoles = ref([])
const currentUserId = ref(null)

const fetchRoles = async () => {
  try {
    const res = await request.get('/api/users/roles')
    allRoles.value = res
  } catch (error) {
    console.error(error)
  }
}

const openRoleDialog = (row) => {
  currentUserId.value = row.id
  selectedRoles.value = row.roles.map(r => r.id)
  roleDialogVisible.value = true
}

const saveRoles = async () => {
  roleLoading.value = true
  try {
    await request.post(`/api/users/${currentUserId.value}/roles`, { role_ids: selectedRoles.value })
    ElMessage.success('角色分配成功')
    roleDialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error(error)
  } finally {
    roleLoading.value = false
  }
}

onMounted(() => {
  fetchData()
  fetchRoles()
})
</script>