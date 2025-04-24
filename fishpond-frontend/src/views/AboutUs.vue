<template>
  <div class="about-us-container">
    <!-- 版本信息区域 -->
    <div class="version-info-section">
      <div class="header-content">
        <div class="image-container">
          <img src="@/assets/brand.png" alt="brand" class="responsive-image"/>
        </div>
      </div>

      <div class="version-buttons">
        <button class="version-button update-button" @click="showUpdateTip">版本升级</button>
        <button class="version-button log-button" @click="showChangeLog">查看升级日志</button>
      </div>

      <div class="current-version">
        <span class="version-label">当前版本：</span>
        <span class="version-number">v2.1.0</span>
      </div>

      <div class="project-info">
        <div class="project-title">
          慧水产养殖系统
        </div>
        <div class="project-members">
          指导老师：管华、雷用敏 || 组长：胡智坤 || 成员：刘希文、汪润、梁婧怡、刘焱平
        </div>
      </div>
    </div>

    <!-- 版本升级提示弹窗 -->
    <Transition name="fade">
      <div class="modal" v-if="isUpdateTipVisible">
        <Transition name="popup">
          <div class="modal-content">
            <div class="modal-header">
              <h3>版本提示</h3>
              <span class="close-btn" @click="isUpdateTipVisible = false">&times;</span>
            </div>
            <div class="modal-body">
              <!-- 加载中状态 -->
              <div v-if="isLoading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>检查更新中...</p>
              </div>
              <!-- 已是最新版本提示 -->
              <p v-else>已经是最新版本了</p>
            </div>
            <div class="modal-footer">
              <button class="confirm-btn" @click="isUpdateTipVisible = false">确定</button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>

    <!-- 升级日志弹窗 -->
    <Transition name="fade">
      <div class="modal" v-if="isChangeLogVisible">
        <Transition name="popup">
          <div class="modal-content changelog-content">
            <div class="modal-header">
              <h3>升级日志</h3>
              <span class="close-btn" @click="isChangeLogVisible = false">&times;</span>
            </div>
            <div class="modal-body">
              <div class="changelog">
                <div class="changelog-item">
                  <h4>v2.1.0 (当前版本)</h4>
                  <ul>
                    <li>新增水质实时监控大屏展示</li>
                    <li>优化传感器数据采集稳定性</li>
                    <li>改进数据图表展示效果</li>
                    <li>修复若干已知问题</li>
                  </ul>
                </div>
                <div class="changelog-item">
                  <h4>v2.0.0</h4>
                  <ul>
                    <li>全新界面设计，提升用户体验</li>
                    <li>增加多设备管理功能</li>
                    <li>支持远程控制和参数设置</li>
                    <li>增强系统安全性</li>
                  </ul>
                </div>
                <div class="changelog-item">
                  <h4>v1.5.0</h4>
                  <ul>
                    <li>增加数据导出功能</li>
                    <li>优化响应速度和性能</li>
                    <li>新增用户权限管理</li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="confirm-btn" @click="isChangeLogVisible = false">关闭</button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import {Monitor, SetUp, DataAnalysis, Connection} from '@element-plus/icons-vue'
import { ref } from 'vue'

// 弹窗控制变量
const isUpdateTipVisible = ref(false)
const isChangeLogVisible = ref(false)
const isLoading = ref(false)

// 显示版本升级提示
const showUpdateTip = () => {
  isLoading.value = true
  isUpdateTipVisible.value = true
  
  // 0.5秒后隐藏加载状态
  setTimeout(() => {
    isLoading.value = false
  }, 500)
}

// 显示升级日志
const showChangeLog = () => {
  isChangeLogVisible.value = true
}
</script>

<style scoped>
.about-us-container {
  padding: 10px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 版本信息样式 */
.version-info-section {
  margin-bottom: 40px;
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.logo-container {
  margin-bottom: 20px;
}

.version-logo {
  width: 80px;
  height: 80px;
}

.version-buttons {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  width: 100%;
  max-width: 500px;
  justify-content: center;
}

.version-button {
  padding: 10px 0;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  width: 100%;
  transition: all 0.3s ease;
}

.update-button {
  background-color: #dc3545;
  color: white;
}

.log-button {
  background-color: #17a2b8;
  color: white;
}

.current-version {
  margin-bottom: 20px;
  font-size: 16px;
}

.version-number {
  font-weight: bold;
  color: #333;
}

.project-info {
  text-align: center;
  width: 100%;
}

.project-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
}

.project-members {
  font-size: 14px;
  color: #666;
}

.about-section {
  margin-bottom: 40px;
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 22px;
  color: #101828;
  margin-bottom: 20px;
  position: relative;
  padding-bottom: 10px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 3px;
  background-color: #5E6AD2;
  border-radius: 3px;
}

.about-content {
  color: #667085;
  line-height: 1.6;
}

.advantage-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.advantage-card {
  background-color: #f9f9ff;
  padding: 24px;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s ease;
}

.advantage-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(94, 106, 210, 0.1);
}

.advantage-icon {
  font-size: 36px;
  color: #5E6AD2;
  margin-bottom: 16px;
}

.advantage-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #101828;
}

.advantage-card p {
  color: #667085;
  font-size: 14px;
}

.team-info {
  margin-top: 20px;
}

.team-section {
  margin-bottom: 30px;
}

.team-section h3 {
  font-size: 18px;
  color: #101828;
  margin-bottom: 15px;
  border-left: 3px solid #5E6AD2;
  padding-left: 10px;
}

.member-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.member-card {
  display: flex;
  align-items: center;
  padding: 16px;
  background-color: #f9f9ff;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.member-card:hover {
  background-color: #f0f1ff;
}

.member-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #e0e2f7;
  margin-right: 16px;
  flex-shrink: 0;
}

.member-info h4 {
  margin: 0 0 5px 0;
  color: #101828;
  font-size: 16px;
}

.member-info p {
  margin: 0;
  color: #667085;
  font-size: 14px;
}

.content-layout {
  display: flex;
  flex-direction: row;
  gap: 30px;
  align-items: center;
}

.content-left {
  flex: 0 0 300px;
}

.content-left img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.content-right {
  flex: 1;
}

.image-gallery {
  display: flex;
  flex-direction: row;
  gap: 20px;
  justify-content: space-between;
  width: 100%;
}

.gallery-item {
  flex: 1;
  max-width: calc(33.33% - 14px);
}

.gallery-item img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.gallery-item img:hover {
  transform: scale(1.03);
}

@media (max-width: 768px) {
  .advantage-cards, .member-list {
    grid-template-columns: 1fr;
  }

  .content-layout {
    flex-direction: column;
  }

  .content-left {
    flex: 0 0 auto;
    margin-bottom: 20px;
  }

  .image-gallery {
    flex-direction: column;
    gap: 15px;
  }

  .gallery-item {
    max-width: 100%;
  }
}

.responsive-image {
  max-width: 80%;
  height: auto;
  margin-bottom: 10px;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 70%;
  margin: 0 auto;
}

.header-content {
  margin-bottom: 10px;
}

.copyright-info {
  text-align: center;
  color: #667085;
  font-size: 14px;
  margin-bottom: 20px;
}

/* 弹窗样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.changelog-content {
  max-width: 600px;
}

.modal-header {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.modal-footer {
  padding: 15px 20px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #eee;
}

.confirm-btn {
  padding: 8px 20px;
  background-color: #5E6AD2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* 升级日志样式 */
.changelog {
  color: #333;
}

.changelog-item {
  margin-bottom: 20px;
}

.changelog-item h4 {
  color: #5E6AD2;
  margin: 0 0 10px 0;
  padding-bottom: 5px;
  border-bottom: 1px solid #eee;
}

.changelog-item ul {
  margin: 0;
  padding-left: 20px;
}

.changelog-item li {
  margin-bottom: 8px;
  line-height: 1.5;
}

/* 弹窗动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.popup-enter-active,
.popup-leave-active {
  transition: all 0.3s ease;
}

.popup-enter-from,
.popup-leave-to {
  transform: scale(0.8);
  opacity: 0;
}

/* 加载中图标样式 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #5E6AD2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
