<template>
  <div class="about-us-container">
    <div class="about-section">
      <h2 class="section-title">智能养鱼解决方案</h2>
      <div class="about-content">
        <p>我们致力于将先进的物联网技术应用于水产养殖领域，打造智能化、数字化的现代养殖模式。通过实时监控水质参数、自动化控制设备以及数据分析，我们的系统能够有效提高养殖效率、降低风险、增加产量。</p>
        <p>我们的系统实现了全天候的水质监测，包括温度、pH值、溶解氧、氨氮等关键参数，并根据鱼类生长需求，自动调节水环境，保障鱼类健康成长。</p>
      </div>
    </div>

    <div class="about-section">
      <h2 class="section-title">核心优势</h2>
      <div class="advantage-cards">
        <div class="advantage-card">
          <el-icon class="advantage-icon"><Monitor /></el-icon>
          <h3>实时监控</h3>
          <p>全天候监测水质参数，及时预警异常情况</p>
        </div>
        <div class="advantage-card">
          <el-icon class="advantage-icon"><SetUp /></el-icon>
          <h3>智能控制</h3>
          <p>自动化调节系统，维持最佳养殖环境</p>
        </div>
        <div class="advantage-card">
          <el-icon class="advantage-icon"><DataAnalysis /></el-icon>
          <h3>数据分析</h3>
          <p>深度分析养殖数据，优化养殖策略</p>
        </div>
        <div class="advantage-card">
          <el-icon class="advantage-icon"><Connection /></el-icon>
          <h3>远程管理</h3>
          <p>随时随地监控和管理养殖环境</p>
        </div>
      </div>
    </div>

    <div class="about-section">
      <h2 class="section-title">团队介绍</h2>
      <div class="team-info">
        <div class="team-section">
          <h3>指导老师</h3>
          <div class="member-list">
            <div class="member-card">
              <div class="member-info">
                <h4>管华</h4>
              </div>
            </div>
            <div class="member-card">
              <div class="member-info">
                <h4>雷用敏</h4>
              </div>
            </div>
          </div>
        </div>

        <div class="team-section">
          <h3>核心成员</h3>
          <div class="member-list">
            <div class="member-card">
              <div class="member-info">
                <h4>胡智坤</h4>
                <p>项目负责人，系统架构师</p>
              </div>
            </div>
            <div class="member-card">
              <div class="member-info">
                <h4>刘希文</h4>
                <p>硬件工程师，传感器专家</p>
              </div>
            </div>
            <div class="member-card">
              <div class="member-info">
                <h4>汪润</h4>
                <p>软件工程师，前端开发</p>
              </div>
            </div>
            <div class="member-card">
              <div class="member-info">
                <h4>刘焱平</h4>
                <p>数据分析师，算法专家</p>
              </div>
            </div>
            <div class="member-card">
              <div class="member-info">
                <h4>梁婧怡</h4>
                <p>美术设计师，视频创作</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Monitor, SetUp, DataAnalysis, Connection } from '@element-plus/icons-vue'
</script>

<style scoped>
.about-us-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
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

@media (max-width: 768px) {
  .advantage-cards, .member-list {
    grid-template-columns: 1fr;
  }
}
</style> 