
-- ChatGPT 自动提问脚本
-- 将剪贴板内容发送到 ChatGPT

tell application "ChatGPT"
    activate
    delay 2  -- 等待应用启动
end tell

tell application "System Events"
    delay 1  -- 等待窗口加载
    
    -- 获取剪贴板内容
    set the clipboard to "我是管理学博士生，研究题目是'AI服务失误对消费者信任的影响'，核心假设是：AI的某些'失误'可能产生意外积极的结果（如Serendipity、Pratfall Effect）。

我已经设计了5个情境实验：
A. 意外创意：AI失误→更好的创意
B. 幽默对话：AI幽默回答荒谬问题  
C. 诚实道歉：AI承认错误
D. 意外功能：AI给得比预期多
E. 对照组：无失误

请帮我：
1. 评估这些情境是否有效捕捉核心假设
2. 推荐成熟量表测量意外惊喜、拟人化、信任
3. 建议如何优化问卷题目
4. 指出实验设计的不足之处"
    
    -- 粘贴内容（Command+V）
    keystroke "v" using {command down}
    delay 1
    
    -- 按回车发送
    key code 36  -- Return key
    delay 1
end tell

display notification "已向 ChatGPT 发送问题！" with title "ChatGPT Automation"

