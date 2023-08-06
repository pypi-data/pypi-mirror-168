# TODO

序列化类：
- `is_active`在序列化类exclude。计划把`is_active`定义为一个内部标签，`False`对外返回一个特殊状态`is_active=False`，且数据不可直接访问。
- Version表的`id`字段、关联Model的字段一般也可以不要。
- 

模型类：
- 允许直接访问ModelVersion的Field。比如`course.title`代替`courses.versions.latest('version').title`。
- 定义QuerySet的delete方法。不知道怎么关联到Manager。
- [自定义`is_active`标记](custom_is_active_field.md)。
- `on_delete`选项不知道是否对关联逻辑的实现有什么影响，还需要评审。
