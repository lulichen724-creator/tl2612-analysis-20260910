现行追加：美股指数与七姐妹两个板块已纳入全站；用户要求历史仅本地，当前dist移除history.html与reports历史文件，旧版本先按精确提交字节备份到私有work。日更打包使用scripts/global_release.py。

# 现行生产配置（2026-11-13）

主站：https://equity-bond-analysis.pages.dev/
项目equity-bond-analysis；旧项目tl-bond-analysis保留为兼容镜像及历史入口。
两者连接现有GitHub仓库lulichen724-creator/tl2612-analysis-20260910，main分支、None框架、exit 0构建、dist输出。
仅公开dist白名单成品；研究后台与原始数据不公开。唯一调度与验收见FUSION_DAILY_RUNBOOK.md。
新项目上线以实际生产部署与全站字节核验记录为准，记录位于私有work/fusion/交易日/。

以下为原TL站初始接入记录，旧点位与展示描述仅属历史，不作为今后研究或发布要求。

# Cloudflare Pages 接入

状态：GitHub授权及首次生产部署完成。已用浏览器验证固定网址能显示最新看板、9月11日收盘116.05、11项点位及第4浪标注。首次短暂522，刷新后恢复。

生产网址：https://tl-bond-analysis.pages.dev/
首次部署：c69ecb0e-d75e-425f-9ca0-02df1722172e；源提交2a5e97d。控制台显示Automatic deployments enabled。

Git集成仓库：lulichen724-creator/tl2612-analysis-20260910
生产分支：main
项目名：tl-bond-analysis
框架：None
构建命令：exit 0
输出目录：dist

仅发布dist；禁止发布work、原始数据、凭据或研究后台。选择Pages的Git集成，不使用一次性上传替代每日自动发布。Cloudflare首次授权只选择本仓库即可。部署后记录实际pages.dev域名并验证data-dashboard版本、收盘日期及图表。未验证前继续明确标为迁移待完成。

最新展示：全部展开、结构与形态前移、第4浪着色标出、点位11项一至两句意义；计算方法与来源后台保留不展示。成交核心不得机械切成三价区间，当前保留116.34/115.85估算峰参考（后续每日重算，不固定历史点位）。
