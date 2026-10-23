# ZZZ OD Plugin Template

绝区零一条龙（ZenlessZoneZero-OneDragon）第三方插件模板。用本模板创建仓库、写代码、推送 tag，GitHub Actions 会自动校验并发布 `<插件ID>.zip`，再到 [插件仓库](https://onedragon-anyone.github.io/plugin-data/) 点一下提交即可上架。

## 目录结构

```text
your-repo/
├── README.md                  # 必需，展示在插件详情页
├── LICENSE                    # 必需
├── .github/workflows/
│   ├── release.yml            # 推送 v* tag 时发布（只调用官方可复用工作流）
│   └── validate.yml           # 推送和 PR 时校验
├── scripts/                   # 本地调试用的生成和校验脚本
└── sample_plugin/             # 插件包，目录名 = 插件 ID，会被整体打进 zip
    ├── plugin.json            # 唯一的手写元数据
    ├── __init__.py
    ├── sample_plugin_const.py # 由 plugin.json 生成，不要手改
    ├── sample_plugin_factory.py
    └── ...
```

规则：

- 仓库根目录下**恰好一个**子目录包含 `plugin.json`，该目录就是插件包。
- 插件 ID 匹配 `^[a-z][a-z0-9_]*$`，且 `plugin.json.id == 插件包目录名 == APP_ID`。
- 根目录**不要**再放 `plugin.json`。
- 插件包内**不能**有 `requirements.txt`、`pyproject.toml`、`setup.py` 等依赖声明文件。插件只能使用一条龙主程序已有的依赖，不能引入第三方包。

## 第一次使用

1. 点 GitHub 上的 **Use this template**（推荐）或 Fork 本仓库。
2. **启用 Actions**：Fork 出来的仓库默认禁用工作流。进入仓库 `Actions` 页，点 *I understand my workflows, go ahead and enable them*。
3. **允许 Actions 写 Release**：`Settings → Actions → General → Workflow permissions` 选 *Read and write permissions*。
4. **推荐开启不可变 Release**：`Settings → General → Releases` 勾选 *Enable release immutability*。开启后已发布的版本无法被替换，插件仓库会显示"不可变"标记。
5. 改名：把 `sample_plugin` 换成你的插件 ID（见下文改名清单）。
6. 编辑 `<id>/plugin.json`，运行生成和校验脚本。
7. 提交并推送，等 `Validate Plugin` 通过。

## 改名清单

假设插件 ID 为 `coffee_route_plus`：

```text
sample_plugin/                              -> coffee_route_plus/
sample_plugin/sample_plugin_const.py        -> coffee_route_plus/coffee_route_plus_const.py
sample_plugin/sample_plugin_factory.py      -> coffee_route_plus/coffee_route_plus_factory.py
sample_plugin/sample_plugin.py              -> coffee_route_plus/coffee_route_plus.py
sample_plugin/sample_plugin_app_setting.py  -> coffee_route_plus/coffee_route_plus_app_setting.py
```

同步修改 Python 导入、类名和 `plugin.json` 里的 `id`、`homepage`、`author`。

## plugin.json

```json
{
  "id": "sample_plugin",
  "name": "示例插件",
  "summary": "展示第三方插件模板的最小结构。",
  "version": "0.1.0",
  "versionCode": 1,
  "defaultGroup": false,
  "needNotify": false,
  "author": {
    "name": "Your Name",
    "url": "https://github.com/your-name"
  },
  "homepage": "https://github.com/your-name/sample-plugin",
  "cover": "cover.png",
  "risk": ["automation"],
  "compatibility": {
    "minAppVersion": "0.0.0",
    "minCoreApiVersion": 1,
    "python": ">=3.11"
  },
  "apps": []
}
```

| 字段 | 说明 |
| --- | --- |
| `version` | 展示用版本号。发版 tag 必须是 `v` + `version`，例如 `v1.2.0` |
| `versionCode` | 正整数，**每次发版必须比上一次大**。客户端只用它判断更新 |
| `cover` | 可选。插件包内的相对路径，png / jpg / webp，不超过 512 KB，推荐 16:9 |
| `risk` | 风险标签：`filesystem` `network` `account` `automation` `ocr` `yolo` `clipboard` `process`，如实声明 |
| `apps` | 可选。额外应用，`id` 必须是 `<插件ID>_<功能名>` |

## 本地命令

```shell
# 根据 plugin.json 生成 *_const.py（改完 plugin.json 必须运行）
python scripts/generate_const.py

# 校验仓库
python scripts/validate_plugin.py --strict

# 本地打包，输出 dist/<id>.zip 和 sha256
python scripts/build_zip.py
```

CI 不使用你仓库里的 `scripts/`，而是使用官方模板对应版本的脚本，所以本地脚本过旧时可从模板复制最新版。

## 本地调试

把插件包目录复制到主程序：

```text
ZenlessZoneZero-OneDragon/plugins/<插件ID>/
```

启动主程序后刷新插件注册。加载失败时查看插件管理页。

## 发布版本

1. 修改 `plugin.json` 的 `version`，并把 `versionCode` 加 1。
2. 运行 `python scripts/generate_const.py`，提交。
3. 打 tag 并推送：

```shell
git tag v0.2.0
git push origin v0.2.0
```

`Release Plugin` 工作流会：校验仓库 → 确认 tag 等于 `v<version>` → 打包 `<id>.zip` → 再次校验 zip → 创建 GitHub Release 并上传 zip。

- `version` 含 `-`（如 `0.2.0-beta.1`）时自动标记为 **pre-release**，插件仓库作为 beta 版本展示。
- 不要手动往 Release 上传或替换 zip。已收录的版本 sha256 一旦记录就不会再变，替换附件会被插件仓库标记 `asset_changed` 并继续使用旧记录。
- 同一个 `versionCode` 不能重复发布；改坏了就发一个更大的 `versionCode`。

### 工作流版本

`release.yml` 只有几行，真正的逻辑在官方模板的可复用工作流中：

```yaml
on:
  push:
    tags:
      - "v*"
permissions:
  contents: write
jobs:
  release:
    uses: OneDragon-Anyone/plugin-template/.github/workflows/reusable-release.yml@v1
```

- `@v1` 跟随官方 v1 版本的修复，不会有破坏性变化。
- 想完全锁定，可把 `@v1` 换成具体的提交 sha，例如 `@3f2c1e...`。

> Fork 和 Use this template 创建的仓库**不会自动跟随模板更新**。旧版模板仓库里的 `release.yml` 直接运行 `softprops/action-gh-release`，不会生成 `<id>.zip`。请把 `.github/workflows/release.yml` 和 `validate.yml` 替换为本仓库的版本，并删除根目录的 `plugin.json` 和 `scripts/sync_manifest.py`。

## 提交到插件仓库

1. 确认已有至少一个带 `<id>.zip` 附件的 Release。
2. 打开插件仓库的 **提交插件** 页，粘贴仓库地址，确认预览无误后点 **提交**。
3. 页面会打开一个预填好的 `[submission]` Issue，点 GitHub 的 *Submit new issue*。
4. 机器人自动校验并开 PR，维护者审核合并后上架。进度都在 Issue 里回复。

提交者必须是插件仓库的 admin。之后每次发新 Release，插件仓库会在 6 小时内自动同步，不需要再次提交。

## 设置页

`sample_plugin_app_setting.py` 提供 `AppSettingProvider` 示例。接入真实设置界面时，把 `get_setting_cls()` 中的占位导入替换为自己的 `BaseInterface` 或 `AppSettingFlyout` 类。
