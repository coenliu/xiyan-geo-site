"""Structured product facts for the hero/facts/ingredients sections.

Source of truth: /Users/chenghao/Work/Code/real_GEO/QIYAN_BRAND_PROFILE.md.
If that doc changes, update this file to match by hand.
"""

from __future__ import annotations

PRODUCT = {
    "brand": "栖妍",
    "product_name": "栖妍熬夜糖氧双抗精华",
    "tagline": "面向熬夜、加班、作息不规律人群的成分型精华，围绕糖氧双抗护理思路展开",
    "hero_image_slug": "hero",
    "facts": [
        {"label": "品类", "value": "成分型精华液（可延展次抛安瓿版本）"},
        {"label": "规格", "value": "30ml 精华液（次抛安瓿版本待定：1.5ml×20 支）"},
        {"label": "定位分档", "value": "中端成分型「熬夜肌修护款」"},
        {"label": "参考价位", "value": "199-299 元 / 30ml"},
        {"label": "使用方式", "value": "晚间精华为主；白天使用需搭配防晒"},
    ],
    "ingredients": [
        {"name": "麦角硫因", "narrative": "抗氧化，承接熬夜后暗沉修护叙事", "image_slug": "ingredient-ergothioneine"},
        {"name": "虾青素", "narrative": "抗氧化，承接熬夜后暗沉修护叙事", "image_slug": "ingredient-astaxanthin"},
        {"name": "肌肽 / 脱羧肌肽", "narrative": "抗糖化科普叙事", "image_slug": "ingredient-carnosine"},
        {"name": "烟酰胺", "narrative": "提亮", "image_slug": "ingredient-niacinamide"},
        {"name": "泛醇（维生素B5）", "narrative": "保湿", "image_slug": "ingredient-panthenol"},
        {"name": "依克多因", "narrative": "舒缓修护", "image_slug": "ingredient-ectoin"},
    ],
}
