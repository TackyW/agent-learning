from pydantic import BaseModel, Field, ValidationError, ConfigDict


class PaperInfo(BaseModel):
    # 这个model_config 是 BaseModel中有的属性
    # 如果你对这个PaperInfo有其他的更多的要求 可以重新配置
    """
    extra：控制当传入的数据包含模型中未定义的字段时该怎么办。
        'ignore'（默认）：直接忽略多余的字段。
        'forbid'：直接报错。这在做严格的数据校验时很有用。
        'allow'：允许并保存这些额外字段。
    from_attributes：这个你很可能用到。如果你想把一个普通的 Python 对象（比如从数据库查出来的 ORM 对象）直接转成 Pydantic 模型，需要设置 from_attributes=True。
    frozen：设为 True 后，模型实例就变成了“不可变”的（类似常量），你不能修改它的属性值。
    strict：开启严格模式。默认情况下 Pydantic 会尝试把字符串 "123" 转成整数 123；如果设为 strict=True，类型不匹配就会直接报错
    populate_by_name=True：开启后，你的发过来的属性名可以是下划线形式 也可以是 驼峰形式
    """
    model_config = ConfigDict(
        strict=True,
        extra="forbid"
    )

    title: str = Field(min_length=1)
    authors: list[str]
    year: int = Field(ge=1950, le=2026)
    keywords: list[str]


paper_data = {
    "title": "基于深度学习的图像分类",
    "authors": ["张三", "李四"],
    "year": 2024,
    "keywords": ["CNN", "图像识别"]
}

try:
    # model_validate:用来验证是否满足你所定义的模型
    paper = PaperInfo.model_validate(paper_data)

    print("验证成功！")
    print(paper.title)
    print(paper.year)
    print(paper.model_dump())

except ValidationError as e:
    print("数据验证失败：")
    print(e)
