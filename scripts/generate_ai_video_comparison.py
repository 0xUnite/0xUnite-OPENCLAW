#!/usr/bin/env python3
"""
AI短剧视频生成平台对比报告
生成 PDF 文档 - 专家审核版
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 注册中文字体
def register_chinese_font():
    """注册中文字体"""
    import platform
    system = platform.system()
    
    if system == 'Darwin':
        font_paths = [
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/PingFang.ttc',
            '/Library/Fonts/Arial Unicode.ttf',
        ]
    else:
        font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/System/Library/Fonts/Hiragino Sans GB.ttc',
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                return 'ChineseFont'
            except:
                pass
    
    return 'Helvetica'

def create_pdf():
    """创建对比报告PDF"""
    font_name = register_chinese_font()
    
    doc = SimpleDocTemplate(
        "/Users/sudi/.openclaw/workspace/AI短剧视频生成平台对比报告.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontName=font_name, fontSize=24, spaceAfter=30, alignment=TA_CENTER)
    heading1_style = ParagraphStyle('CustomHeading1', parent=styles['Heading1'], fontName=font_name, fontSize=18, spaceAfter=12, spaceBefore=20)
    heading2_style = ParagraphStyle('CustomHeading2', parent=styles['Heading2'], fontName=font_name, fontSize=14, spaceAfter=10, spaceBefore=15)
    body_style = ParagraphStyle('CustomBody', parent=styles['BodyText'], fontName=font_name, fontSize=11, spaceAfter=8, leading=16)
    highlight_style = ParagraphStyle('Highlight', parent=styles['BodyText'], fontName=font_name, fontSize=12, spaceAfter=8, leading=18, textColor=colors.HexColor('#2563EB'))
    warning_style = ParagraphStyle('Warning', parent=styles['BodyText'], fontName=font_name, fontSize=11, spaceAfter=8, leading=16, textColor=colors.HexColor('#DC2626'))
    
    story = []
    
    # ==================== 封面 ====================
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("AI短剧视频生成平台", title_style))
    story.append(Paragraph("对比分析报告", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("2026年主流平台质量、价格、成本全面对比", body_style))
    story.append(Paragraph("适用于小说推文、AI短剧创作", body_style))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("生成日期：2026年4月 | 专家审核版", body_style))
    story.append(PageBreak())
    
    # ==================== 1. 执行摘要 ====================
    story.append(Paragraph("1. 执行摘要", heading1_style))
    
    summary_text = """
    本报告对比了2026年主流AI视频生成平台在AI短剧制作场景下的表现。
    ⚠️ 重要提示：Sora已于2026年3月25日关闭，本报告不包含Sora。
    """
    story.append(Paragraph(summary_text.strip(), body_style))
    
    summary_data = [
        ['优先级', '平台', '核心理由', '推荐度'],
        ['🥇 首选', '可灵AI (Kling)', '免费额度高、中文优化好、2分钟长视频支持', '★★★★★'],
        ['🥇 首选', '即梦AI (Jimeng)', '免费额度高、字节出品、中文理解能力最强', '★★★★★'],
        ['🥈 次选', 'Seedance 2.0', '质量顶级、字节生态、抖音完美适配', '★★★★☆'],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*cm, 4*cm, 7*cm, 2.5*cm])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#DCFCE7')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#DCFCE7')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())
    
    # ==================== 2. 平台概览 ====================
    story.append(Paragraph("2. 平台概览与核心能力", heading1_style))
    
    overview_text = """
    本次对比涵盖5个当前可用的AI视频生成平台，重点评估其对小说推文和AI短剧创作的适用性。
    """
    story.append(Paragraph(overview_text.strip(), body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # 平台概览表
    overview_data = [
        ['平台', '出品方', '最新版本', '核心定位', '最大时长'],
        ['可灵AI', '快手', '3.0', '国内AI视频领军，支持长视频', '2分钟 ★'],
        ['即梦AI', '字节跳动', '3.0', '中文理解最强，界面友好', '5秒'],
        ['Seedance 2.0', '字节跳动', '2.0', '视频生成DeepSeek时刻', '10秒'],
        ['Veo 3.1', 'Google', '3.1', '全球质量领先，音画同步优秀', '8秒'],
        ['海螺AI', 'MiniMax', '2.3', '国际市场排名靠前', '6秒'],
    ]
    
    overview_table = Table(overview_data, colWidths=[2.5*cm, 2.5*cm, 2*cm, 5.5*cm, 2.5*cm])
    overview_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#DCFCE7')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#DCFCE7')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 0.5*cm))
    
    advantage_note = """
    <b>💡 关键优势：可灵AI是目前唯一支持2分钟长视频生成的免费/低成本平台，</b>
    对于需要连续叙事的AI短剧来说，这是核心差异点。
    """
    story.append(Paragraph(advantage_note.strip().replace('\n', '<br/>'), highlight_style))
    story.append(PageBreak())
    
    # ==================== 3. 功能对比 ====================
    story.append(Paragraph("3. 核心功能对比", heading1_style))
    
    func_text = """
    以下是各平台在AI短剧制作中核心功能的对比：
    """
    story.append(Paragraph(func_text.strip(), body_style))
    story.append(Spacer(1, 0.3*cm))
    
    func_data = [
        ['功能', '可灵AI', '即梦AI', 'Seedance', 'Veo 3.1', '海螺AI'],
        ['文生视频', '✅', '✅', '✅', '✅', '✅'],
        ['图生视频', '✅', '✅', '✅', '✅', '✅'],
        ['对口型', '✅ ★', '✅', '❌', '✅', '✅'],
        ['运镜控制', '✅', '✅', '✅', '✅', '✅'],
        ['角色一致性', '✅', '✅', '✅', '✅', '✅'],
        ['中文理解', '★★★★', '★★★★★', '★★★★', '★★★', '★★★★'],
        ['免费额度', '66积分/天', '60-100积分/天', '少量试用', '少量试用', '少量试用'],
    ]
    
    func_table = Table(func_data, colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    func_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F3F4F6')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(func_table)
    story.append(Spacer(1, 0.3*cm))
    
    func_note = """
    <b>说明：</b>对口型是小说推文的核心功能，可灵AI在此项表现最佳。
    即梦AI的中文理解能力在所有维度中评分最高。
    """
    story.append(Paragraph(func_note.strip(), body_style))
    story.append(PageBreak())
    
    # ==================== 4. 质量对比 ====================
    story.append(Paragraph("4. 视频质量对比", heading1_style))
    
    quality_text = """
    以下是各平台在视频质量方面的专业评估：
    """
    story.append(Paragraph(quality_text.strip(), body_style))
    story.append(Spacer(1, 0.3*cm))
    
    quality_data = [
        ['评估维度', '可灵AI 3.0', '即梦AI 3.0', 'Seedance 2.0', 'Veo 3.1', '海螺AI'],
        ['画面真实感', '★★★★☆', '★★★★☆', '★★★★★', '★★★★★', '★★★★☆'],
        ['动作流畅度', '★★★★☆', '★★★★☆', '★★★★★', '★★★★★', '★★★★☆'],
        ['角色一致性', '★★★★☆', '★★★★☆', '★★★★★', '★★★★☆', '★★★★☆'],
        ['光影效果', '★★★★☆', '★★★★☆', '★★★★★', '★★★★★', '★★★★☆'],
        ['中文场景适配', '★★★★★', '★★★★★', '★★★★★', '★★★☆☆', '★★★★☆'],
        ['物理规律准确性', '★★★★☆', '★★★★☆', '★★★★★', '★★★★★', '★★★★☆'],
        ['综合评分', '★★★★☆', '★★★★☆', '★★★★★', '★★★★★', '★★★★☆'],
    ]
    
    quality_table = Table(quality_data, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    quality_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FEF3C7')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(quality_table)
    story.append(Spacer(1, 0.5*cm))
    
    quality_note = """
    <b>专家解读：</b><br/>
    1. Seedance 2.0和Veo 3.1在纯视频质量上领先，但价格较高且中文适配略弱<br/>
    2. 可灵AI和即梦AI在中文场景下表现优秀，且都有免费额度<br/>
    3. 对于小说推文，中文理解和角色一致性比极端的物理真实性更重要
    """
    story.append(Paragraph(quality_note.strip().replace('\n', '<br/>'), body_style))
    story.append(PageBreak())
    
    # ==================== 5. 价格对比 ====================
    story.append(Paragraph("5. 价格与成本对比", heading1_style))
    
    price_text = """
    以下是各平台的定价详情（截至2026年4月）：
    """
    story.append(Paragraph(price_text.strip(), body_style))
    story.append(Spacer(1, 0.3*cm))
    
    price_data = [
        ['平台', '免费额度/天', '付费月费', '单秒成本', '60秒(6片段)'],
        ['可灵AI', '66积分≈6个5秒', '¥99-399', '约¥1-2', '¥0(免费)或¥600'],
        ['即梦AI', '60-100积分≈6个5秒', '¥59-299', '约¥0.5-1', '¥0(免费)或¥300'],
        ['Seedance 2.0', '限量试用', '¥199-999', '约¥1', '¥600+'],
        ['Veo 3.1', '限量试用', '$15-75', '$0.15-0.75', '约¥60-400'],
        ['海螺AI', '限量试用', '¥99-399', '约¥1-2', '¥600+'],
    ]
    
    price_table = Table(price_data, colWidths=[2.5*cm, 3.5*cm, 2.5*cm, 2.5*cm, 3*cm])
    price_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#DCFCE7')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#DCFCE7')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(price_table)
    story.append(Spacer(1, 0.5*cm))
    
    # 免费额度说明
    free_note = """
    <b>💰 免费用户最佳策略：</b><br/>
    • 可灵AI：每天66积分，约6个5秒视频 = 1集短剧<br/>
    • 即梦AI：每天60-100积分，约6个5秒视频 = 1集短剧<br/>
    • <b>双平台混用：每天可产出约2集60秒短剧</b><br/>
    <b>结论：可灵+即梦双免费账号 = 零成本AI短剧批量生产</b>
    """
    story.append(Paragraph(free_note.strip().replace('\n', '<br/>'), highlight_style))
    story.append(PageBreak())
    
    # ==================== 6. 性价比分析 ====================
    story.append(Paragraph("6. 性价比综合分析", heading1_style))
    
    value_text = """
    综合考虑视频质量、功能完整性、价格成本、中文适配四大维度：
    """
    story.append(Paragraph(value_text.strip(), body_style))
    story.append(Spacer(1, 0.3*cm))
    
    value_data = [
        ['排名', '平台', '性价比', '理由'],
        ['🥇 1', '可灵AI', '★★★★★', '免费额度高+2分钟长视频+对口型，中文场景最佳选择'],
        ['🥇 1', '即梦AI', '★★★★★', '免费额度高+中文理解最强+界面友好，零成本入门首选'],
        ['🥈 2', 'Seedance 2.0', '★★★★☆', '质量顶级但付费成本高，适合高端制作'],
        ['🥉 3', '海螺AI', '★★★★☆', '国际市场认可度高，但国内版权问题需注意'],
        ['4', 'Veo 3.1', '★★★☆☆', '价格高且国内访问不便，非首选'],
    ]
    
    value_table = Table(value_data, colWidths=[2*cm, 3*cm, 2*cm, 8*cm])
    value_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 2), colors.HexColor('#DCFCE7')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(value_table)
    story.append(PageBreak())
    
    # ==================== 7. 场景化推荐 ====================
    story.append(Paragraph("7. 场景化推荐方案", heading1_style))
    
    # 场景1
    story.append(Paragraph("场景1：新手入门 / 零成本创业", heading2_style))
    s1_text = """
    <b>推荐：即梦AI + 可灵AI 双平台免费版</b><br/>
    优势：零成本、每天可产2集60秒短剧、中文理解优秀<br/>
    预估成本：<b>¥0/月</b><br/>
    适用：验证商业模式、小规模测试、个人副业起步
    """
    story.append(Paragraph(s1_text.strip().replace('\n', '<br/>'), body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # 场景2
    story.append(Paragraph("场景2：规模化生产 / 工作室运营", heading2_style))
    s2_text = """
    <b>推荐：可灵AI会员 + 即梦AI会员 混用</b><br/>
    优势：双平台每天可产4-6集、大量生成视频、更高质量<br/>
    预估成本：<b>¥200-500/月</b><br/>
    适用：稳定产出、批量制作、内容矩阵运营
    """
    story.append(Paragraph(s2_text.strip().replace('\n', '<br/>'), body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # 场景3
    story.append(Paragraph("场景3：高端短剧 / 平台参赛", heading2_style))
    s3_text = """
    <b>推荐：Seedance 2.0 为主 + 可灵AI辅助</b><br/>
    优势：最高视频质量、抖音/字节生态完美适配<br/>
    预估成本：<b>¥1000-3000/月</b><br/>
    适用：抖音短剧大赛、精品内容制作、IP孵化
    """
    story.append(Paragraph(s3_text.strip().replace('\n', '<br/>'), body_style))
    story.append(PageBreak())
    
    # ==================== 8. 结论 ====================
    story.append(Paragraph("8. 结论与建议", heading1_style))
    
    conclusion_text = """
    <b>最终推荐：</b><br/><br/>
    对于<b>小说推文和AI短剧创作</b>，我们的建议是：
    """
    story.append(Paragraph(conclusion_text.strip().replace('\n', '<br/>'), body_style))
    story.append(Spacer(1, 0.3*cm))
    
    final_data = [
        ['用户类型', '推荐方案', '月成本'],
        ['新手/个人', '即梦AI + 可灵AI 免费版', '¥0'],
        ['工作室/团队', '可灵AI会员 + 即梦AI会员', '¥200-500'],
        ['高端制作', 'Seedance 2.0 + 可灵AI混用', '¥1000-3000'],
    ]
    
    final_table = Table(final_data, colWidths=[3.5*cm, 7*cm, 3*cm])
    final_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#DCFCE7')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(final_table)
    story.append(Spacer(1, 1*cm))
    
    # 风险提示
    risk_text = """
    <b>⚠️ 重要提示 (2026年4月更新)：</b><br/>
    1. Sora已于2026年3月25日关闭，本报告已移除<br/>
    2. AI视频平台竞争激烈，建议不要单一依赖某个平台<br/>
    3. 免费额度可能随时调整，请关注官方公告<br/>
    4. 建议优先使用国产平台，避免政策风险<br/>
    5. 可灵AI的2分钟长视频是独特优势，目前无替代
    """
    story.append(Paragraph(risk_text.strip().replace('\n', '<br/>'), warning_style))
    
    doc.build(story)
    print("PDF生成成功！")
    print("文件路径：/Users/sudi/.openclaw/workspace/AI短剧视频生成平台对比报告.pdf")

if __name__ == "__main__":
    create_pdf()
