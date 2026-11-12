# 工具用法与真实输出样例

所有脚本：Python 3.9 兼容、仅标准库、都有 `--help`、随机部分用 `--seed`（默认 42）保证可复现。下面的输出是 2026-11-12 在本机（Python 3.9.6）实际运行的结果。示例配置里的数值是**占位数据，不是行业基准**。

```bash
cd skills/game-design-economy/scripts
python3 -I economy_sim.py --help
```

## 1. economy_sim.py：经济模拟

配置结构（完整例子见 `assets/economy_example.json`）：

| 键 | 含义 |
|---|---|
| `player_types[]` | 玩家类型：`weight`、`sessions_per_day`、`ads_per_day`、`retention`（留存锚点，如 `{"1":0.38,"7":0.12,"30":0.04}`，对数线性插值） |
| `per_session_sources[]` | 每局产出：`amount`、`cv`（波动）、`scale_with_level`（随升级提升） |
| `daily_sources[]` | 每日产出（签到）：`amount`、`probability` |
| `ad_reward_amount` | 每个激励视频的奖励 |
| `per_session_sink` | 每局消耗（消耗品） |
| `ladder` | 升级阶梯：`cost = base_cost * growth ** level` |
| `milestones[]` | 里程碑：到达阶梯某级 |
| `stall_patience_days` / `stall_churn_per_day` | 连续多少天买不起下一级算"卡住"，卡住后每天流失概率 |

注意：`retention` 是**本征留存**（不含卡关造成的额外流失）；卡关流失由 stall 参数叠加。

```bash
python3 -I economy_sim.py --config ../assets/economy_example.json
```

```text
Economy simulation: casual-upgrade-loop (example, placeholder numbers)
players=2000 days=30 seed=42

day     active    act%    bal_med    bal_p90  L_p10  L_med  L_p90  stalled%
1          844   42.2%        128        319    3.0    3.0    6.0      0.0%
3          637   31.9%        312        724    6.0    9.0   11.0      0.0%
7          341   17.1%        674       2500    9.0   13.0   15.0      0.0%
14         263   13.2%       2308       3967   13.0   16.0   19.0      0.0%
30          48    2.4%       1884      10375   17.0   20.5   23.0     33.3%

Time to milestone (ladder level):
  chapter_1    L5    reached by  37.2% of players  median day 2.0  p90 day 3.0
  chapter_2    L12   reached by  18.0% of players  median day 6.0  p90 day 11.0
  chapter_3    L20   reached by   5.5% of players  median day 16.0  p90 day 25.0
  endgame      L35   reached by   0.0% of players  median day: never

Income by source:
  stage_clear         7244377   59.5%
  rewarded_ad         3448350   28.3%
  daily_login         1482200   12.2%
Spend: ladder=10189917 per_session=669600
Players who left because stalled: 5.7% of all simulated players
```

怎么读：
- `bal_p90` 远高于 `bal_med` 且还在涨 = 有人在囤币，说明消耗口不够（或价格太低）。
- `stalled%` 在 D30 达到 33%：活到 D30 的人里三分之一买不起下一级，说明后期阶梯太陡或产出不够；调 `growth` 或 `scale_with_level`。
- `endgame` 没人到达：要么内容设计过深、要么 30 天内本来就不该有人到。**对照设计目标判断**，不是越多越好。
- 常用扫描：改一个参数跑多遍，记录到 `docs/metrics-log.md`。例如 `--players 5000 --days 60 --seed 1..5` 看种子间波动，波动大就加玩家数。
- `--json` 输出可喂给别的工具或表格。

## 2. drop_rate_calc.py：掉率与保底

子命令：`expected`、`prob`、`fifty`、`copies`、`simulate`。模型：基础概率 `rate`；`--soft-start/--soft-step` 软保底（从第 soft-start 抽起每抽加 step）；`--hard-pity` 硬保底。

```bash
python3 -I drop_rate_calc.py expected --rate 0.006 --hard-pity 90 --soft-start 74 --soft-step 0.06
```
```text
rate=0.00600 hard_pity=90 soft_start=74 soft_step=0.0600
pulls to first success             mean=  62.30  median=  76  p90=  80  p99=  83
no-pity expectation 1/rate = 166.67
```

```bash
python3 -I drop_rate_calc.py prob --rate 0.02 --pulls 10 50 100
```
```text
   pulls  P(at least one)
      10   18.29%
      50   63.58%
     100   86.74%
```

50/50 机制（输了下一个必出 UP）：

```bash
python3 -I drop_rate_calc.py fifty --rate 0.006 --hard-pity 90 --soft-start 74 --soft-step 0.06 --featured 0.5
```
```text
any success                        mean=  62.30  median=  76  p90=  80  p99=  83
featured (50/50 mechanic)          mean=  93.45  median=  80  p90= 155  p99= 161

P(featured within N pulls):
  N=30      8.96%
  N=60     17.69%
  N=90     59.39%
  N=120    70.50%
  N=160    98.53%
  N=180   100.00%
worst case with guarantee: 180 pulls
```

蒙特卡洛交叉验证（解析解 93.45 vs 模拟 93.54，50000 次，seed 42）：

```bash
python3 -I drop_rate_calc.py simulate --rate 0.006 --hard-pity 90 --soft-start 74 --soft-step 0.06 --trials 50000 --featured 0.5
```
```text
Monte Carlo trials=50000 seed=42 count=1
mean=93.54 median=80 p90=155 p99=161
```

多份（凑 3 张 UP，每张之后保底重置）：

```bash
python3 -I drop_rate_calc.py copies --rate 0.006 --hard-pity 90 --soft-start 74 --soft-step 0.06 --count 3 --pulls 300 500
```
```text
pulls for 3 featured copies        mean= 280.34  median= 281  p90= 383  p99= 458
  P(>=3 copies within 300 pulls) = 58.41%
  P(>=3 copies within 500 pulls) = 100.00%
```

用法提示：无硬保底时尾部会被截断（最多约 4000 抽，输出会提示）；`--start-pity` 表示"已垫了多少抽"，`--guaranteed` 表示"上次歪了"。

## 3. difficulty_curve.py：难度曲线

形状：`ramp` / `sawtooth` / `stairs` / `wave`。难度分 0–10，线性映射到目标胜率（`--wr-easy 0.92` → `--wr-hard 0.25`，参考映射，按品类校准）。`--param NAME=BASE,SCALE` 生成随难度变化的关卡参数。

```bash
python3 -I difficulty_curve.py --levels 12 --shape sawtooth --period 5 --param moves=30,-0.04
```
```text
level  score  tag       win%     attempts  moves     curve
1      0.58   TUTORIAL  88.1     1.14      29.3      #
2      0.22   TUTORIAL  90.6     1.10      29.74     
3      1.50   TUTORIAL  82.0     1.22      28.2      ###
4      3.18   normal    70.7     1.41      26.18     ######
5      4.94   normal    58.9     1.70      24.08     ##########
6      2.29   RELIEF    76.7     1.30      27.25     #####
7      3.87   normal    66.1     1.51      25.36     ########
8      4.83   normal    59.6     1.68      24.2      ##########
9      6.48   hard      48.6     2.06      22.22     #############
10     9.20   BOSS      30.4     3.29      18.97     ##################
11     5.19   RELIEF    57.2     1.75      23.77     ##########
12     6.82   hard      46.3     2.16      21.82     ##############

levels=12  min=0.22  max=9.20  mean=4.09  boss_levels=[10]
largest level-to-level jump=4.01 (flag if > 2.5 outside bosses)
```

`--csv` / `--json` 可直接导入关卡配置表。这是**目标曲线**，要用 `game-playtest-qa` 的埋点（每关胜率、重试次数）回填实测后再调。
