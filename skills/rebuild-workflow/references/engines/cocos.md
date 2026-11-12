# 引擎：Cocos Creator / cocos2d-x / cocos2d-js（⚠️ 未验证：尚无真实案例，内容为通用知识 + 起步清单）

> 项目首次遇到 Cocos 时边做边填，把「未验证」逐条改成 ✅/🟡 并写案例。国内休闲/小游戏、棋牌、H5 转原生包里很常见。

## 识别特征（S1）
- `lib/*/libcocos2djs.so`（2.x JSB / cocos2d-js）、`libcocos.so`（Creator 3.x）、`libcocos2dcpp.so`（cocos2d-x C++）。`detect_engine.py` 已覆盖。
- JS 层：`assets/src/*.js` 或 `assets/src/*.jsc`、`assets/main.js`、`assets/jsb-adapter/`；Creator 3.x 另有 `assets/assets/<bundle>/{config.<hash>.json,import/,native/}`。
- 版本号：Creator 3.x 在 `assets/src/settings*.json` / `cc.js` 头注释里；2.x 在 `project.json` 或 `main.js` 旁。**以实际文件为准**。

## 源码可恢复性（S1 出口必写）
| 形态 | 结论（初判） | 说明 |
|---|---|---|
| 明文 `.js` | 高 | 美化（prettier/js-beautify）后可读；有 sourcemap 则近乎还原 |
| `.jsc`（加密字节码） | 中 | 常见做法：xxtea 加密（可能再 gzip）；**密钥通常写在 `libcocos2djs.so`**（`jsb_set_xxtea_key` 调用处的字符串）。取密钥属于逆向分析范围，仍受 scope.md「静态分析」勾选约束 |
| C++（cocos2d-x） | 低 | 原生 so，只能做签名/字符串级分析，逻辑按行为重做 |

## 解包与回导工具（S3） → 见 `rebuild-asset-recovery`
| 资源类型 | 工具 | 验证状态 |
|---|---|---|
| 图集 | `.plist + .png`（TexturePacker 格式）直接按 plist 切图；Creator 3.x 为 `.json` 图集配置 | 未验证 |
| 骨骼动画 | Spine（`.json/.skel + .atlas`）、DragonBones（`*_ske.json + *_tex.json`）可直接用官方运行时回放；回导方式同 godot 的 Spine 流程 | 未验证 |
| 音频 | `.mp3/.ogg/.wav` 通常明文；Creator 3.x `native/` 目录下按 uuid 命名，需读 `config.*.json` 里的 uuid→路径映射 | 未验证 |
| 文案 / 配置 | 多为 `import/*.json`（Creator 3.x 部分版本为压缩二进制 `.cconb`，需官方版本的反序列化逻辑） | 未验证 |
| 场景 / Prefab | 在 bundle 的 `import/` 内为序列化 JSON；还原为可编辑的 `.scene` 非官方支持，建议只提取布局信息 | 未验证 |

## 开发（S5）
- 方案选择见 `rebuild-product-design` D 系列决策门：Cocos 包可「继续用 Cocos 重写」或「迁移到 Godot」。迁移成本低的是纯 2D/UI 玩法；依赖 Cocos 特有组件（RichText、ScrollView 适配）时迁移要预留 UI 返工。
- Creator 命令行构建需要对应版本编辑器；**不同小版本 API 有破坏性差异**，M0 必须把版本钉死到 `工具链表`。

## 打包（S7）
- Android 构建链依赖 Creator 的 Build 面板或 `CocosCreator --project <dir> --build "platform=android;..."`；JDK/SDK/NDK 版本必须与 Creator 版本匹配。**未验证**，首次实践后补坑。

## 案例
- （待补）
