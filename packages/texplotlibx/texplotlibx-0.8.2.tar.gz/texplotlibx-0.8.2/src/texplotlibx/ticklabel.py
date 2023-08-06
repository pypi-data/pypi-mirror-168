from .attribute import _tpl_attribute_variable, _tpl_attribute_flag


class _tpl_ticklabel:
  def __init__(self, axis: str):
    if axis not in ('x', 'y'):
      print(f'Cannot interpret axis \"{axis}\" for tick label')
      return None
    self.__axis = axis
    self.__show = False
    self.__precision = _tpl_attribute_variable(token='precision')
    self.__fixed = _tpl_attribute_flag(token='fixed')
    self.__zerofill = _tpl_attribute_flag(token='fixed zerofill')
    self.__fontsize = _tpl_attribute_variable(token='font')
    self.__scaled_ticks = _tpl_attribute_variable(token=f'scaled {axis} ticks')
    self.__ticks = _tpl_attribute_variable(token=f'{axis}tick')
    self.__tick_labels = _tpl_attribute_variable(token=f'{axis}ticklabels')

  def _set_precision(self, prec: int):
    self.__precision.set_value(prec)
    self.__show = True

  def _set_fixed(self, fixed: bool = True):
    self.__fixed.set_value(fixed)
    self.__show = True

  def _set_zerofill(self, zerofill: bool = True):
    self.__zerofill.set_value(zerofill)
    self.__show = True

  def _set_fontsize(self, fontsize: str = '\\large'):
    self.__fontsize.set_value(fontsize)
    self.__show = True

  def _set_scaled(self, scaled_ticks: bool = True):
    self.__scaled_ticks.set_value(scaled_ticks)

  def _set_ticks(self, data: list[float] = None):
    if data is not None:
      lst = '{' + ','.join(map(str, data)) + '}'
      self.__ticks.set_value(lst)
      self.__show = True
    else:
      self.__ticks.set_value(None)

  def _set_ticks_use_data(self, use_data: bool = False):
    if use_data:
      self.__ticks.set_value('data')
    else:
      self.__ticks.set_value(None)
    self.__show = True

  def _set_tick_labels(self, labels: list[str] = None):
    if labels is not None:
      for label in labels:
        if label[0] != '{' or label[-1] != '}':
          label = '{' + label + '}'
      lst = '{' + ','.join(labels) + '}'
      self.__tick_labels.set_value(lst)
      self.__show = True
    else:
      self.__tick_labels.set_value(None)

    {self.__tick_labels}

  def __str__(self):
    tls = f"""{self.__axis} tick label style={{
    /pgf/number format/.cd,
    {self.__fixed}
    {self.__zerofill}
    {self.__precision}
    {self.__fontsize}
    {self.__ticks}
    /tikz/.cd
  }},""" if self.__show else f"% {self.__axis} tick label style"
    return tls + f"\n  {self.__scaled_ticks}"
