from django import template


register = template.Library()


@register.filter()
def label_with_for(value, arg):
    return value.label_tag(attrs={'for': value.id_for_label})


@register.filter()
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})


@register.filter()
def widget_with_classes(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter()
def widget_with_classes_placeholder(value, arg):
    return value.as_widget(attrs={'class': arg, 'placeholder': value.label})

