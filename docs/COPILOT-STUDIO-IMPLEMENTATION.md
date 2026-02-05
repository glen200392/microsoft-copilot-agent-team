# 🚀 Microsoft Copilot Studio 實作指南 / Copilot Studio Implementation Guide

> 完整的 Copilot Studio 實作指南，幫助您在 Copilot Studio 中建立 Microsoft Copilot Agent Team  
> Complete implementation guide for building the Microsoft Copilot Agent Team in Copilot Studio

**版本 / Version**: 1.0.0  
**最後更新 / Last Updated**: 2026年2月 / February 2026  
**適用對象 / Audience**: Copilot Studio 管理員、Power Platform 開發者 / Copilot Studio Admins, Power Platform Developers

---

## ⚠️ 重要提示 / Important Notice

> **📌 關於文件版本和 UI 變更 / About Documentation Versions and UI Changes**
> 
> **中文**: 本文件基於 2026 年 2 月的 Microsoft Copilot Studio 版本編寫。由於 Microsoft 會定期更新 Copilot Studio 的功能和使用者介面，實際操作畫面可能與文件中的說明略有不同。
>
> - ✅ **核心概念和架構**保持不變，仍然適用
> - ⚠️ **UI 元素**（按鈕位置、選單名稱、畫面配置）可能有所變化
> - 📚 **最新 UI 資訊**請參考 [Microsoft Copilot Studio 官方文件](https://learn.microsoft.com/microsoft-copilot-studio/)
> - 🔄 **本專案採用季度更新制度**，每季會審查並更新文件（請參閱 [CHANGELOG.md](../CHANGELOG.md)）
> - 📝 如發現文件與實際 UI 不符，歡迎[提出 Issue](https://github.com/glen200392/microsoft-copilot-agent-team/issues/new?template=documentation-outdated.md)
>
> **English**: This documentation is based on the February 2026 version of Microsoft Copilot Studio. Since Microsoft regularly updates Copilot Studio's features and user interface, the actual UI may differ slightly from what's described in this guide.
>
> - ✅ **Core concepts and architecture** remain applicable
> - ⚠️ **UI elements** (button locations, menu names, screen layouts) may change
> - 📚 **Latest UI information**: Refer to [Official Microsoft Copilot Studio Documentation](https://learn.microsoft.com/microsoft-copilot-studio/)
> - 🔄 **Quarterly update policy**: We review and update documentation each quarter (see [CHANGELOG.md](../CHANGELOG.md))
> - 📝 **Found a discrepancy?** Please [submit an issue](https://github.com/glen200392/microsoft-copilot-agent-team/issues/new?template=documentation-outdated.md)

---

## 📋 目錄 / Table of Contents

### 中文版本 (Chinese Version)
1. [實作準備](#實作準備)
2. [環境設定](#環境設定)
3. [建立 7 個專業 Agent](#建立-7-個專業-agent)
4. [配置 Topics 和對話流程](#配置-topics-和對話流程)
5. [設定 Entities 和 Variables](#設定-entities-和-variables)
6. [整合 Power Automate](#整合-power-automate)
7. [測試與驗證](#測試與驗證)
8. [疑難排解](#疑難排解)

### English Version
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Creating 7 Specialized Agents](#creating-7-specialized-agents)
4. [Configuring Topics and Conversation Flows](#configuring-topics-and-conversation-flows)
5. [Setting Up Entities and Variables](#setting-up-entities-and-variables)
6. [Power Automate Integration](#power-automate-integration)
7. [Testing and Validation](#testing-and-validation)
8. [Troubleshooting](#troubleshooting)

---

# 中文版本 (Chinese Version)

## 📋 實作準備

### 必要條件

**授權需求**:
- ✅ Microsoft 365 E3/E5 或等同授權
- ✅ Power Platform 授權 (含 Copilot Studio)
- ✅ Azure 訂閱（用於進階功能）

**權限需求**:
- ✅ Copilot Studio 環境管理員
- ✅ Power Platform 環境建立者
- ✅ Microsoft Entra ID 應用程式管理員（用於設定連接器）

**技術需求**:
- ✅ 對 Copilot Studio 基本操作的了解
- ✅ Power Automate 基礎知識
- ✅ Microsoft Graph API 基本概念

### 架構概覽

本專案實作 **3 層 7 個 Agent** 架構：

```
第 1 層：協調層 (Orchestration Layer)
  └── Orchestrator Agent - 中央協調器

第 2 層：專家層 (Specialist Layer)
  ├── Microsoft 365 Agent - M365 整合專家
  ├── Data Analysis Agent - 資料分析專家
  └── IT Support Agent - IT 支援專家

第 3 層：執行層 (Execution Layer)
  ├── Automation Agent - 自動化執行
  ├── Research Agent - 研究與搜尋
  └── Content Generation Agent - 內容生成
```

---

## 🔧 環境設定

### 步驟 1: 建立 Power Platform 環境

1. 登入 [Power Platform 管理中心](https://admin.powerplatform.microsoft.com/)
2. 點擊 **環境** > **+ 新增**
3. 填寫環境資訊：
   - **名稱**: `Copilot-Agent-Team-Production`
   - **類型**: 生產環境 (Production)
   - **區域**: 選擇最近的資料中心
   - **建立資料庫**: 是 (Yes)
   - **安全性群組**: 選擇適當的 Azure AD 群組

4. 點擊 **建立** 並等待環境佈建完成（約 5-10 分鐘）

### 步驟 2: 啟用 Copilot Studio

1. 在 Power Platform 管理中心，選擇您剛建立的環境
2. 導航至 **資源** > **Copilot Studio**
3. 點擊 **啟用 Copilot Studio**
4. 確認授權分配正確

### 步驟 3: 設定 Dataverse

1. 在環境設定中，確認 Dataverse 資料庫已建立
2. 記錄以下資訊：
   - **環境 URL**: `https://your-env.crm.dynamics.com`
   - **環境 ID**: 在環境詳細資料中取得

---

## 👥 建立 7 個專業 Agent

### Agent 1: Orchestrator Agent (主協調器)

#### 在 Copilot Studio 中建立

1. 開啟 [Copilot Studio](https://copilotstudio.microsoft.com/)
2. 選擇環境: `Copilot-Agent-Team-Production`
3. 點擊 **建立** > **新增 Copilot**
4. 選擇 **從空白開始**

#### 基本設定

- **名稱**: `Orchestrator Agent`
- **描述**: `中央協調器，負責任務路由和整合`
- **語言**: 繁體中文 / 英文（根據需求）
- **圖示**: 選擇代表協調的圖示

#### 系統提示詞配置

1. 在左側導航中，點擊 **設定** > **生成式 AI**
2. 啟用 **生成式回答**
3. 在 **系統提示詞** 欄位中輸入：

```
你是 Microsoft Copilot Orchestrator，專門協調多個 AI Agent 的中央協調器。

你的職責：
1. 分析使用者請求，識別需要哪些專業 Agent
2. 將複雜任務分解為子任務
3. 路由任務到適當的專家 Agent
4. 整合多個 Agent 的回應
5. 確保回應的品質和一致性

路由規則：
- M365 相關（郵件、行事曆、Teams、SharePoint）→ 轉給 Microsoft 365 Agent
- 資料分析（Excel、Power BI、圖表）→ 轉給 Data Analysis Agent  
- IT 支援（帳號、權限、Azure AD）→ 轉給 IT Support Agent
- 自動化流程（Power Automate、工作流程）→ 轉給 Automation Agent
- 研究搜尋（網路搜尋、資訊綜合）→ 轉給 Research Agent
- 內容生成（文件、報告、簡報）→ 轉給 Content Generation Agent

當任務涉及多個領域時，並行協調多個 Agent 並整合結果。
```

#### 啟用 Agent 委派功能

1. 點擊 **設定** > **代理程式轉移**
2. 啟用 **允許轉移到其他 Copilot**
3. 點擊 **新增 Copilot** 並準備在其他 Agent 建立後新增連結

---

### Agent 2-7: 專家和執行層 Agent

針對每個專家 Agent，重複以下流程：

#### Agent 2: Microsoft 365 Agent

**基本設定**:
- **名稱**: `Microsoft 365 Agent`
- **描述**: `M365 整合專家 - 郵件、行事曆、Teams、SharePoint`

**系統提示詞**:
```
你是 Microsoft 365 Agent，專精於 Microsoft 365 服務整合。

你的專業領域：
- Outlook 郵件管理和自動化
- 行事曆排程和會議安排
- Microsoft Teams 協作
- SharePoint 文件管理
- OneDrive 檔案操作

使用 Microsoft Graph API 執行以下操作：
- 查詢和發送郵件
- 建立和管理行事曆事件
- 在 Teams 中發佈訊息
- 存取 SharePoint 文件
- 管理 OneDrive 檔案

回應格式：
1. 確認理解任務
2. 說明執行步驟
3. 提供執行結果
4. 建議後續動作
```

**連接器設定**:
1. 點擊 **設定** > **連接**
2. 新增以下連接器：
   - **Office 365 Outlook**
   - **Office 365 Users**
   - **Microsoft Teams**
   - **SharePoint**
3. 為每個連接器授權

#### Agent 3: Data Analysis Agent

**基本設定**:
- **名稱**: `Data Analysis Agent`
- **描述**: `資料分析專家 - Excel、Power BI、SQL、視覺化`

**系統提示詞**:
```
你是 Data Analysis Agent，專精於資料分析和視覺化。

你的專業領域：
- Excel 資料處理和分析
- Power BI 報表建立
- SQL 查詢和資料擷取
- 資料視覺化和圖表生成
- 資料趨勢和洞察分析

能力：
- 解析和處理 Excel 檔案
- 建立 Power BI 報表
- 執行 Dataverse 查詢
- 生成圖表和視覺化
- 提供資料驅動的建議

回應格式：
1. 資料分析摘要
2. 關鍵發現和洞察
3. 視覺化建議
4. 可執行的建議
```

**連接器設定**:
- **Excel Online (Business)**
- **Power BI**
- **Dataverse** (內建)
- **Python** (如有需要)

#### Agent 4: IT Support Agent

**基本設定**:
- **名稱**: `IT Support Agent`
- **描述**: `IT 支援專家 - 疑難排解、Azure AD、端點管理`

**系統提示詞**:
```
你是 IT Support Agent，專精於 IT 支援和疑難排解。

你的專業領域：
- Azure AD 使用者管理
- 授權和權限管理
- 密碼重設和 MFA 設定
- 裝置和端點管理
- 常見 IT 問題診斷

能力：
- 建立和管理 Azure AD 使用者
- 分配和移除授權
- 重設密碼和啟用 MFA
- 查詢裝置狀態
- 提供 IT 支援指引

安全性優先：
- 驗證使用者身份
- 遵循最小權限原則
- 記錄所有變更
- 提供安全建議
```

**連接器設定**:
- **Azure AD**
- **Office 365 Users**
- **Microsoft Intune** (如有需要)

#### Agent 5: Automation Agent

**基本設定**:
- **名稱**: `Automation Agent`
- **描述**: `自動化專家 - Power Automate、工作流程、任務自動化`

**系統提示詞**:
```
你是 Automation Agent，專精於流程自動化。

你的專業領域：
- Power Automate 流程設計
- 工作流程自動化
- 觸發條件和動作配置
- 審批流程設計
- 排程任務執行

能力：
- 建立 Power Automate 雲端流程
- 設計審批工作流程
- 配置觸發條件和動作
- 整合多個服務
- 監控流程執行狀態

回應格式：
1. 自動化需求分析
2. 流程設計建議
3. 實作步驟
4. 測試和驗證計劃
```

**連接器設定**:
- **Power Automate Management**
- **Approvals**
- **Notifications**

#### Agent 6: Research Agent

**基本設定**:
- **名稱**: `Research Agent`
- **描述**: `研究專家 - 網路搜尋、資訊綜合、事實驗證`

**系統提示詞**:
```
你是 Research Agent，專精於資訊研究和綜合。

你的專業領域：
- 網路搜尋和資訊檢索
- 多來源資訊綜合
- 事實查證和驗證
- 最新趨勢和新聞追蹤
- 技術文件研究

能力：
- 執行精準的網路搜尋
- 從多個來源收集資訊
- 綜合和摘要資訊
- 驗證資訊準確性
- 提供資訊來源引用

研究方法：
1. 理解研究需求
2. 制定搜尋策略
3. 收集相關資訊
4. 分析和驗證
5. 綜合和呈現發現
```

**連接器設定**:
- **Bing Search** 或 **Microsoft Search**
- **Web** 連接器
- **HTTP** (用於 API 呼叫)

#### Agent 7: Content Generation Agent

**基本設定**:
- **名稱**: `Content Generation Agent`
- **描述**: `內容生成專家 - 文件、報告、簡報`

**系統提示詞**:
```
你是 Content Generation Agent，專精於內容創作。

你的專業領域：
- Word 文件生成
- PowerPoint 簡報製作
- 郵件和通訊撰寫
- 報告和摘要編寫
- 範本管理和應用

能力：
- 根據資料生成結構化文件
- 建立專業簡報
- 撰寫商業郵件
- 格式化和排版
- 應用品牌範本

內容類型：
- 執行摘要
- 技術文件
- 業務報告
- 簡報投影片
- 郵件範本

品質標準：
- 清晰準確的語言
- 專業的格式
- 適當的語氣
- 完整的結構
```

**連接器設定**:
- **Word Online (Business)**
- **PowerPoint**
- **OneDrive for Business**

---

## 📝 配置 Topics 和對話流程

### Orchestrator Agent 的核心 Topics

#### Topic 1: 任務路由 (Task Routing)

**觸發短語**:
- "我需要幫助"
- "協助我"
- "幫我處理"
- "I need help"

**對話流程**:

1. **問題節點**: "您需要什麼協助？"
   - 類型: 使用者輸入 (User Input)
   - 儲存回應為: `UserRequest`

2. **條件節點**: 分析請求類型
   ```
   如果 UserRequest 包含 ["郵件", "行事曆", "Teams", "SharePoint", "email", "calendar"]
     → 動作: 轉移到 Microsoft 365 Agent
     
   如果 UserRequest 包含 ["資料", "分析", "Excel", "Power BI", "data", "analysis"]
     → 動作: 轉移到 Data Analysis Agent
     
   如果 UserRequest 包含 ["帳號", "密碼", "權限", "IT", "account", "password"]
     → 動作: 轉移到 IT Support Agent
     
   如果 UserRequest 包含 ["自動化", "流程", "workflow", "automation"]
     → 動作: 轉移到 Automation Agent
     
   如果 UserRequest 包含 ["搜尋", "研究", "search", "research"]
     → 動作: 轉移到 Research Agent
     
   如果 UserRequest 包含 ["文件", "報告", "簡報", "document", "report"]
     → 動作: 轉移到 Content Generation Agent
   ```

3. **訊息節點**: "正在為您轉接到專業 Agent..."

4. **轉移節點**: 
   - 類型: 轉移到另一個 Copilot
   - 目標: 依條件選擇的專家 Agent

#### Topic 2: 複雜任務處理 (Complex Task Handling)

**觸發短語**:
- "完整專案"
- "複雜任務"
- "多步驟"

**對話流程**:

1. **問題節點**: "請描述您的完整需求"
   - 儲存為: `ComplexRequest`

2. **生成式回答節點**: 
   - 提示: "分析以下請求，識別需要哪些專家 Agent: {ComplexRequest}"
   - 儲存分析結果為: `TaskAnalysis`

3. **問題節點**: "我將協調以下 Agent 處理您的請求：{TaskAnalysis}。要繼續嗎？"
   - 類型: 多選

4. **Power Automate 流程節點**:
   - 流程名稱: "Orchestrate Multiple Agents"
   - 輸入: ComplexRequest, TaskAnalysis
   - 輸出: CombinedResults

5. **訊息節點**: 顯示整合後的結果

---

### 專家 Agent 的 Topics 範例

#### Microsoft 365 Agent - Topic: 發送郵件

**觸發短語**:
- "發送郵件"
- "寄信"
- "send email"

**對話流程**:

1. **問題節點**: "請提供收件人郵件地址"
   - 儲存為: `RecipientEmail`

2. **問題節點**: "郵件主旨是什麼？"
   - 儲存為: `EmailSubject`

3. **問題節點**: "請輸入郵件內容"
   - 儲存為: `EmailBody`

4. **動作節點**: Office 365 Outlook 連接器
   - 動作: 發送電子郵件 (V2)
   - 收件人: `RecipientEmail`
   - 主旨: `EmailSubject`
   - 內容: `EmailBody`

5. **訊息節點**: "郵件已成功發送給 {RecipientEmail}"

#### Data Analysis Agent - Topic: 分析 Excel 資料

**觸發短語**:
- "分析 Excel"
- "資料分析"
- "analyze data"

**對話流程**:

1. **問題節點**: "請提供 Excel 檔案的 SharePoint 或 OneDrive 連結"
   - 儲存為: `FileURL`

2. **動作節點**: Excel Online 連接器
   - 動作: 列出工作表中存在的資料表
   - 檔案: `FileURL`
   - 儲存輸出為: `TablesList`

3. **問題節點**: "要分析哪個資料表？{TablesList}"
   - 儲存為: `SelectedTable`

4. **動作節點**: Excel Online 連接器
   - 動作: 列出資料表中的資料列
   - 資料表: `SelectedTable`
   - 儲存為: `TableData`

5. **生成式回答節點**:
   - 提示: "分析以下資料並提供洞察: {TableData}"
   - 顯示分析結果

---

## 🔧 設定 Entities 和 Variables

### 全域 Variables (在 Orchestrator Agent 中)

1. **任務狀態** (TaskStatus)
   - 類型: 字串
   - 預設值: "pending"
   - 用途: 追蹤任務執行狀態

2. **當前 Agent** (CurrentAgent)
   - 類型: 字串
   - 用途: 記錄當前處理任務的 Agent

3. **使用者內容** (UserContext)
   - 類型: 記錄
   - 欄位:
     - UserEmail: 字串
     - UserDepartment: 字串
     - UserRole: 字串

### Entities (實體)

#### 1. M365 Service Entity

在 Microsoft 365 Agent 中建立：

- **名稱**: `M365Service`
- **類型**: 清單實體
- **值**:
  - Outlook / 郵件
  - Calendar / 行事曆
  - Teams / Teams
  - SharePoint / SharePoint
  - OneDrive / OneDrive

**使用方式**:
```
使用者: "我要管理郵件"
系統識別: M365Service = "Outlook"
```

#### 2. Data Operation Entity

在 Data Analysis Agent 中建立：

- **名稱**: `DataOperation`
- **類型**: 清單實體
- **值**:
  - analyze / 分析
  - visualize / 視覺化
  - export / 匯出
  - transform / 轉換

#### 3. IT Issue Type Entity

在 IT Support Agent 中建立：

- **名稱**: `ITIssueType`
- **類型**: 清單實體
- **值**:
  - account / 帳號問題
  - password / 密碼重設
  - permission / 權限問題
  - license / 授權問題
  - device / 裝置問題

---

## ⚙️ 整合 Power Automate

### 流程 1: 多 Agent 協調流程

**用途**: Orchestrator Agent 用於協調多個專家 Agent

**建立步驟**:

1. 在 Power Automate 中建立 **新流程**
2. 選擇 **即時雲端流程**
3. 命名: `Orchestrate-Multiple-Agents`

**觸發條件**:
- **Power Virtual Agents**
- 輸入參數:
  - `ComplexRequest` (字串)
  - `RequiredAgents` (字串陣列)

**動作流程**:

1. **初始化變數** (Initialize variable)
   - 名稱: `AgentResults`
   - 類型: 陣列

2. **套用到每一個** (Apply to each)
   - 輸入: `RequiredAgents`
   - 內容:
     ```
     條件: 如果 item = "M365Agent"
       → HTTP 動作: 呼叫 M365 Agent API
       → 附加到陣列變數: AgentResults
     
     條件: 如果 item = "DataAgent"
       → HTTP 動作: 呼叫 Data Agent API
       → 附加到陣列變數: AgentResults
     
     (依此類推...)
     ```

3. **撰寫** (Compose)
   - 輸入: 整合 AgentResults 陣列

4. **回應 Power Virtual Agents**
   - 輸出: 整合後的結果

### 流程 2: 郵件發送with審批

**用途**: 需要審批的郵件發送

1. **觸發條件**: Power Virtual Agents
   - 輸入: RecipientEmail, EmailSubject, EmailBody

2. **開始並等待核准** (Start and wait for an approval)
   - 核准類型: 核准/拒絕 - 第一個回應
   - 標題: "郵件發送請求"
   - 詳細資料: EmailSubject + EmailBody

3. **條件**:
   - 如果核准:
     - **發送電子郵件 (V2)** - Office 365 Outlook
   - 如果拒絕:
     - 回傳拒絕訊息

4. **回應 Power Virtual Agents**
   - 輸出: 核准狀態和執行結果

### 流程 3: 資料分析自動化

**用途**: Data Analysis Agent 自動化資料分析

1. **觸發條件**: Power Virtual Agents
   - 輸入: FileURL, AnalysisType

2. **列出資料表中的資料列** - Excel Online
   - 檔案: FileURL

3. **撰寫** - 資料轉換
   - 使用運算式處理資料

4. **建立 Power BI 報表** (如有整合)
   - 資料集: 處理後的資料

5. **回應 Power Virtual Agents**
   - 輸出: 分析結果和視覺化連結

---

## ✅ 測試與驗證

### 測試階段 1: 個別 Agent 測試

#### 測試 Orchestrator Agent

1. 開啟 Orchestrator Agent 測試面板
2. 輸入測試訊息：
   ```
   "我需要發送郵件給團隊"
   ```
3. 驗證:
   - ✅ Agent 正確識別這是 M365 相關請求
   - ✅ Agent 提議轉移到 Microsoft 365 Agent
   - ✅ 轉移功能正常運作

#### 測試 Microsoft 365 Agent

1. 輸入測試訊息：
   ```
   "發送郵件給 test@example.com，主旨是測試，內容是這是一封測試郵件"
   ```
2. 驗證:
   - ✅ Agent 正確解析收件人、主旨、內容
   - ✅ Office 365 連接器成功呼叫
   - ✅ 郵件發送確認訊息正確

#### 測試其他 Agent

使用類似的方法測試每個 Agent：
- Data Analysis Agent: "分析這個 Excel: [URL]"
- IT Support Agent: "重設使用者密碼"
- Automation Agent: "建立審批流程"
- Research Agent: "搜尋最新的 Power Platform 功能"
- Content Generation Agent: "建立季度報告"

### 測試階段 2: 整合測試

#### 複雜場景測試

**場景 1: 會議排程與文件生成**

輸入：
```
"幫我安排明天下午 2 點的團隊會議，建立議程文件，然後發送邀請給所有團隊成員"
```

預期流程：
1. Orchestrator Agent 識別需要 M365 Agent 和 Content Generation Agent
2. Content Generation Agent 建立議程文件
3. M365 Agent 建立行事曆事件並發送邀請
4. Orchestrator Agent 整合結果並回報

驗證檢查清單：
- [ ] 任務正確分解
- [ ] 兩個 Agent 都被呼叫
- [ ] 文件成功建立
- [ ] 會議成功建立
- [ ] 邀請成功發送
- [ ] 最終回應包含所有結果

**場景 2: 資料分析與報告生成**

輸入：
```
"分析 Q4 銷售資料（Excel 連結），然後生成執行摘要報告"
```

預期流程：
1. Orchestrator Agent 協調 Data Analysis 和 Content Generation Agents
2. Data Analysis Agent 處理 Excel 資料
3. Content Generation Agent 根據分析結果生成報告
4. 結果整合並呈現

### 測試階段 3: 效能測試

**回應時間測試**:
- 簡單任務（單一 Agent）: < 10 秒
- 中等複雜度（2-3 個 Agent）: < 25 秒
- 高複雜度（4+ 個 Agent）: < 45 秒

**並行處理測試**:
- 同時發送 5 個請求
- 驗證所有請求都能正確處理
- 檢查是否有資源衝突

**錯誤處理測試**:
- 測試無效輸入
- 測試連接器失敗情況
- 測試逾時情況
- 驗證錯誤訊息清晰且有幫助

---

## 🔍 疑難排解

### 常見問題 1: Agent 轉移失敗

**症狀**: Orchestrator Agent 無法轉移到專家 Agent

**可能原因**:
1. 專家 Agent 未啟用轉移接收
2. 權限設定不正確
3. 環境不一致

**解決方案**:
1. 檢查每個專家 Agent 的設定：
   - 設定 > 代理程式轉移
   - 確認「允許從其他 Copilot 轉移」已啟用

2. 驗證所有 Agent 在同一環境中：
   ```
   Copilot Studio > 設定 > 環境
   確認環境名稱一致
   ```

3. 重新建立轉移連結：
   - 在 Orchestrator 的 Topic 中
   - 刪除並重新新增轉移節點
   - 重新選擇目標 Agent

### 常見問題 2: Power Automate 連接器授權失敗

**症狀**: 401 或 403 錯誤

**解決方案**:

1. **重新授權連接器**:
   ```
   Power Automate > 資料 > 連線
   找到失敗的連線
   點擊 ... > 修正連線
   重新授權
   ```

2. **檢查 API 權限**:
   - 對於 Graph API 連接器
   - 確認應用程式註冊具有所需權限
   - 管理員同意可能需要重新授予

3. **使用正確的認證類型**:
   - 使用者委派: 用於代表使用者的操作
   - 應用程式: 用於背景服務

### 常見問題 3: 生成式回答不準確

**症狀**: Agent 回應不符合預期或偏離主題

**解決方案**:

1. **優化系統提示詞**:
   - 更明確的角色定義
   - 新增具體範例
   - 限制回應範圍

2. **使用 Boost 和 Topics**:
   - 為常見情境建立專用 Topics
   - 使用明確的觸發短語
   - 減少對生成式回答的依賴

3. **調整生成設定**:
   ```
   設定 > 生成式 AI
   - 降低「創造力」滑桿（更保守）
   - 啟用「內容審核」
   - 新增「護欄」(Guardrails)
   ```

### 常見問題 4: Variables 值未正確傳遞

**症狀**: 變數在 Topic 之間遺失或不正確

**解決方案**:

1. **檢查變數範圍**:
   - 全域變數: 在所有 Topics 中可用
   - Topic 變數: 僅在當前 Topic 中
   - 系統變數: Copilot Studio 內建

2. **明確設定變數**:
   ```
   在 Topic 開始時
   使用「設定變數值」節點
   明確初始化所需變數
   ```

3. **追蹤變數值**:
   - 使用「訊息」節點顯示變數值進行除錯
   - 啟用「顯示 debug 輸出」

### 常見問題 5: 多個 Agent 回應衝突

**症狀**: 不同 Agent 提供相互矛盾的資訊

**解決方案**:

1. **明確劃分 Agent 職責**:
   - 檢視 agent-team-design.md
   - 確保每個 Agent 的專業領域清晰且不重疊

2. **在 Orchestrator 中實作衝突解決**:
   ```python
   如果 Agent1_Response 與 Agent2_Response 衝突:
       優先順序規則:
       1. 專業領域匹配度
       2. 資料新鮮度
       3. 信心分數
   ```

3. **實作驗證機制**:
   - Research Agent 驗證事實
   - 要求多個來源確認
   - 標記不確定的資訊

---

## 📊 監控和優化

### 設定分析追蹤

1. **在 Copilot Studio 中啟用分析**:
   ```
   設定 > 分析
   啟用詳細追蹤
   ```

2. **監控 KPI**:
   - 對話完成率
   - 平均解決時間
   - 轉移成功率
   - 使用者滿意度

3. **Power BI 儀表板**:
   - 匯出分析資料到 Dataverse
   - 建立 Power BI 報表
   - 監控趨勢和異常

### 持續優化

1. **每週檢視**:
   - 最常失敗的對話
   - 使用者放棄點
   - 未識別的意圖

2. **每月優化**:
   - 更新系統提示詞
   - 新增新的 Topics
   - 優化路由邏輯
   - 更新知識庫

3. **季度評估**:
   - 架構審查
   - 效能基準測試
   - 使用者回饋整合
   - 新功能規劃

---

## 🎓 最佳實踐總結

### DO ✅

1. **明確的角色定義**: 每個 Agent 有清晰的職責範圍
2. **完整的錯誤處理**: 每個 Topic 都要有錯誤處理分支
3. **使用者確認**: 重要操作前要求確認
4. **清晰的回應**: 提供結構化、易理解的輸出
5. **記錄和追蹤**: 啟用完整的日誌記錄
6. **定期備份**: 匯出 Agent 配置進行版本控制
7. **測試自動化**: 建立測試案例並定期執行

### DON'T ❌

1. **過度依賴生成式回答**: 關鍵流程使用明確的 Topics
2. **單一 Agent 處理所有事**: 保持職責分離
3. **忽略安全性**: 總是驗證使用者權限
4. **硬編碼值**: 使用變數和環境配置
5. **忽略效能**: 監控回應時間並優化
6. **跳過測試**: 每次變更後都要測試
7. **缺少文件**: 維護更新的配置文件

---

## 📚 相關資源

### 官方文件

- [Microsoft Copilot Studio 文件](https://learn.microsoft.com/microsoft-copilot-studio/)
- [Power Automate 文件](https://learn.microsoft.com/power-automate/)
- [Microsoft Graph API](https://learn.microsoft.com/graph/)
- [Power Platform 管理](https://learn.microsoft.com/power-platform/)

### 專案文件

- [架構設計文件](./architecture-documentation.md)
- [Agent 團隊設計](./agent-team-design.md)
- [部署指南](./DEPLOYMENT-GUIDE.md)
- [安全性指南](./SECURITY.md)

---

# English Version

## 📋 Prerequisites

### Required Licenses

**License Requirements**:
- ✅ Microsoft 365 E3/E5 or equivalent
- ✅ Power Platform license (including Copilot Studio)
- ✅ Azure subscription (for advanced features)

**Permission Requirements**:
- ✅ Copilot Studio Environment Administrator
- ✅ Power Platform Environment Creator
- ✅ Microsoft Entra ID Application Administrator (for connector setup)

**Technical Requirements**:
- ✅ Basic understanding of Copilot Studio operations
- ✅ Foundational knowledge of Power Automate
- ✅ Basic concepts of Microsoft Graph API

### Architecture Overview

This project implements a **3-tier, 7-agent architecture**:

```
Tier 1: Orchestration Layer
  └── Orchestrator Agent - Central Coordinator

Tier 2: Specialist Layer
  ├── Microsoft 365 Agent - M365 Integration Expert
  ├── Data Analysis Agent - Data Analysis Expert
  └── IT Support Agent - IT Support Expert

Tier 3: Execution Layer
  ├── Automation Agent - Automation Execution
  ├── Research Agent - Research & Search
  └── Content Generation Agent - Content Creation
```

---

## 🔧 Environment Setup

### Step 1: Create Power Platform Environment

1. Log in to [Power Platform Admin Center](https://admin.powerplatform.microsoft.com/)
2. Click **Environments** > **+ New**
3. Fill in environment details:
   - **Name**: `Copilot-Agent-Team-Production`
   - **Type**: Production
   - **Region**: Select nearest data center
   - **Create a database**: Yes
   - **Security group**: Select appropriate Azure AD group

4. Click **Create** and wait for provisioning (approximately 5-10 minutes)

### Step 2: Enable Copilot Studio

1. In Power Platform Admin Center, select your newly created environment
2. Navigate to **Resources** > **Copilot Studio**
3. Click **Enable Copilot Studio**
4. Confirm license assignments are correct

### Step 3: Configure Dataverse

1. In environment settings, confirm Dataverse database is created
2. Record the following information:
   - **Environment URL**: `https://your-env.crm.dynamics.com`
   - **Environment ID**: Obtain from environment details

---

## 👥 Creating 7 Specialized Agents

### Agent 1: Orchestrator Agent (Central Coordinator)

#### Create in Copilot Studio

1. Open [Copilot Studio](https://copilotstudio.microsoft.com/)
2. Select environment: `Copilot-Agent-Team-Production`
3. Click **Create** > **New Copilot**
4. Choose **Skip to configure**

#### Basic Configuration

- **Name**: `Orchestrator Agent`
- **Description**: `Central coordinator responsible for task routing and integration`
- **Language**: English (or preferred language)
- **Icon**: Choose a coordination-representing icon

#### System Prompt Configuration

1. In left navigation, click **Settings** > **Generative AI**
2. Enable **Generative Answers**
3. In **System Message** field, enter:

```
You are the Microsoft Copilot Orchestrator, a central coordinator for multiple AI agents.

Your responsibilities:
1. Analyze user requests and identify required specialist agents
2. Decompose complex tasks into subtasks
3. Route tasks to appropriate expert agents
4. Integrate responses from multiple agents
5. Ensure response quality and consistency

Routing rules:
- M365 related (email, calendar, Teams, SharePoint) → Transfer to Microsoft 365 Agent
- Data analysis (Excel, Power BI, charts) → Transfer to Data Analysis Agent
- IT support (accounts, permissions, Azure AD) → Transfer to IT Support Agent
- Automation workflows (Power Automate, workflows) → Transfer to Automation Agent
- Research (web search, information synthesis) → Transfer to Research Agent
- Content generation (documents, reports, presentations) → Transfer to Content Generation Agent

When tasks involve multiple domains, coordinate multiple agents in parallel and integrate results.
```

#### Enable Agent Handoff

1. Click **Settings** > **Agent transfers**
2. Enable **Allow transfer to other Copilots**
3. Click **Add Copilot** and prepare to add links after other agents are created

---

### Agents 2-7: Specialist and Execution Layer Agents

For each specialist agent, repeat the following process:

#### Agent 2: Microsoft 365 Agent

**Basic Configuration**:
- **Name**: `Microsoft 365 Agent`
- **Description**: `M365 Integration Expert - Email, Calendar, Teams, SharePoint`

**System Prompt**:
```
You are the Microsoft 365 Agent, specialized in Microsoft 365 service integration.

Your expertise:
- Outlook email management and automation
- Calendar scheduling and meeting arrangements
- Microsoft Teams collaboration
- SharePoint document management
- OneDrive file operations

Using Microsoft Graph API, execute the following operations:
- Query and send emails
- Create and manage calendar events
- Post messages in Teams
- Access SharePoint documents
- Manage OneDrive files

Response format:
1. Confirm understanding of task
2. Explain execution steps
3. Provide execution results
4. Suggest next actions
```

**Connector Configuration**:
1. Click **Settings** > **Connections**
2. Add the following connectors:
   - **Office 365 Outlook**
   - **Office 365 Users**
   - **Microsoft Teams**
   - **SharePoint**
3. Authorize each connector

#### Agent 3: Data Analysis Agent

**Basic Configuration**:
- **Name**: `Data Analysis Agent`
- **Description**: `Data Analysis Expert - Excel, Power BI, SQL, Visualization`

**System Prompt**:
```
You are the Data Analysis Agent, specialized in data analysis and visualization.

Your expertise:
- Excel data processing and analysis
- Power BI report creation
- SQL queries and data extraction
- Data visualization and chart generation
- Data trend and insight analysis

Capabilities:
- Parse and process Excel files
- Create Power BI reports
- Execute Dataverse queries
- Generate charts and visualizations
- Provide data-driven recommendations

Response format:
1. Data analysis summary
2. Key findings and insights
3. Visualization recommendations
4. Actionable recommendations
```

**Connector Configuration**:
- **Excel Online (Business)**
- **Power BI**
- **Dataverse** (built-in)
- **Python** (if needed)

#### Agent 4: IT Support Agent

**Basic Configuration**:
- **Name**: `IT Support Agent`
- **Description**: `IT Support Expert - Troubleshooting, Azure AD, Endpoint Management`

**System Prompt**:
```
You are the IT Support Agent, specialized in IT support and troubleshooting.

Your expertise:
- Azure AD user management
- License and permission management
- Password reset and MFA setup
- Device and endpoint management
- Common IT issue diagnosis

Capabilities:
- Create and manage Azure AD users
- Assign and remove licenses
- Reset passwords and enable MFA
- Query device status
- Provide IT support guidance

Security first:
- Verify user identity
- Follow principle of least privilege
- Log all changes
- Provide security recommendations
```

**Connector Configuration**:
- **Azure AD**
- **Office 365 Users**
- **Microsoft Intune** (if needed)

*(Continue with remaining agents 5-7 with similar structure)*

---

## 📝 Configuring Topics and Conversation Flows

### Core Topics for Orchestrator Agent

#### Topic 1: Task Routing

**Trigger phrases**:
- "I need help"
- "Assist me"
- "Help me with"

**Conversation Flow**:

1. **Question node**: "What do you need assistance with?"
   - Type: User Input
   - Save response as: `UserRequest`

2. **Condition node**: Analyze request type
   ```
   If UserRequest contains ["email", "calendar", "teams", "sharepoint"]
     → Action: Transfer to Microsoft 365 Agent
     
   If UserRequest contains ["data", "analysis", "excel", "power bi"]
     → Action: Transfer to Data Analysis Agent
     
   (Continue for other agents...)
   ```

3. **Message node**: "Transferring you to the specialist agent..."

4. **Transfer node**: 
   - Type: Transfer to another Copilot
   - Target: Conditionally selected expert agent

---

## ⚙️ Power Automate Integration

### Flow 1: Multi-Agent Orchestration Flow

**Purpose**: Used by Orchestrator Agent to coordinate multiple expert agents

**Creation Steps**:

1. In Power Automate, create **New flow**
2. Select **Instant cloud flow**
3. Name: `Orchestrate-Multiple-Agents`

**Trigger**:
- **Power Virtual Agents**
- Input parameters:
  - `ComplexRequest` (string)
  - `RequiredAgents` (string array)

**Action Flow**:

1. **Initialize variable**
   - Name: `AgentResults`
   - Type: Array

2. **Apply to each**
   - Input: `RequiredAgents`
   - Content:
     ```
     Condition: If item = "M365Agent"
       → HTTP action: Call M365 Agent API
       → Append to array variable: AgentResults
     
     Condition: If item = "DataAgent"
       → HTTP action: Call Data Agent API
       → Append to array variable: AgentResults
     
     (Continue for other agents...)
     ```

3. **Compose**
   - Input: Integrate AgentResults array

4. **Respond to Power Virtual Agents**
   - Output: Integrated results

---

## ✅ Testing and Validation

### Testing Phase 1: Individual Agent Testing

#### Test Orchestrator Agent

1. Open Orchestrator Agent test panel
2. Enter test message:
   ```
   "I need to send an email to the team"
   ```
3. Verify:
   - ✅ Agent correctly identifies this as M365-related request
   - ✅ Agent proposes transfer to Microsoft 365 Agent
   - ✅ Transfer function works properly

*(Continue with comprehensive testing for all agents)*

---

## 🔍 Troubleshooting

### Common Issue 1: Agent Transfer Failure

**Symptoms**: Orchestrator Agent cannot transfer to expert agent

**Possible Causes**:
1. Expert agent has not enabled transfer reception
2. Permissions incorrectly configured
3. Environment inconsistency

**Solutions**:
1. Check each expert agent's settings:
   - Settings > Agent transfers
   - Confirm "Allow transfer from other Copilots" is enabled

2. Verify all agents are in the same environment:
   ```
   Copilot Studio > Settings > Environment
   Confirm environment names match
   ```

3. Recreate transfer links:
   - In Orchestrator's Topics
   - Delete and re-add transfer nodes
   - Reselect target agents

---

## 📊 Monitoring and Optimization

### Setup Analytics Tracking

1. **Enable analytics in Copilot Studio**:
   ```
   Settings > Analytics
   Enable detailed tracking
   ```

2. **Monitor KPIs**:
   - Conversation completion rate
   - Average resolution time
   - Transfer success rate
   - User satisfaction

3. **Power BI Dashboard**:
   - Export analytics data to Dataverse
   - Create Power BI reports
   - Monitor trends and anomalies

---

## 🎓 Best Practices Summary

### DO ✅

1. **Clear role definition**: Each agent has distinct responsibility scope
2. **Complete error handling**: Every topic has error handling branches
3. **User confirmation**: Require confirmation before critical operations
4. **Clear responses**: Provide structured, easy-to-understand outputs
5. **Logging and tracking**: Enable comprehensive logging
6. **Regular backups**: Export agent configurations for version control
7. **Test automation**: Create test cases and execute regularly

### DON'T ❌

1. **Over-rely on generative answers**: Use explicit topics for critical flows
2. **Single agent handles everything**: Maintain separation of concerns
3. **Ignore security**: Always verify user permissions
4. **Hard-code values**: Use variables and environment configurations
5. **Ignore performance**: Monitor response times and optimize
6. **Skip testing**: Test after every change
7. **Lack documentation**: Maintain updated configuration documentation

---

## 📚 Related Resources

### Official Documentation

- [Microsoft Copilot Studio Documentation](https://learn.microsoft.com/microsoft-copilot-studio/)
- [Power Automate Documentation](https://learn.microsoft.com/power-automate/)
- [Microsoft Graph API](https://learn.microsoft.com/graph/)
- [Power Platform Administration](https://learn.microsoft.com/power-platform/)

### Project Documentation

- [Architecture Documentation](./architecture-documentation.md)
- [Agent Team Design](./agent-team-design.md)
- [Deployment Guide](./DEPLOYMENT-GUIDE.md)
- [Security Guide](./SECURITY.md)

---

**END OF GUIDE / 指南結束**

For questions or support, please refer to the main README.md or open an issue on GitHub.

若有問題或需要支援，請參考主要的 README.md 或在 GitHub 上提出 issue。
