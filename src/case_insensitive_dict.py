class CaseInsensitiveDict(dict):
    """
    Case insensitive dict that recursively converts nested dicts.
    """

    def __init__(self, data):
        self.proxy = {}
        for key, value in data.items():
            # Сохраняем оригинальный ключ для proxy
            lower_key = key.lower()
            if lower_key in self.proxy:
                raise ValueError(f"Duplicate key: {key} (case-insensitive)")
            self.proxy[lower_key] = key

            # Рекурсивно преобразуем вложенные словари и списки
            if isinstance(value, dict):
                self[key] = CaseInsensitiveDict(value)
            elif isinstance(value, list):
                self[key] = self._convert_list(value)
            else:
                self[key] = value

    def _convert_list(self, lst):
        """Рекурсивно преобразует списки с вложенными dict"""
        result = []
        for item in lst:
            if isinstance(item, dict):
                result.append(CaseInsensitiveDict(item))
            elif isinstance(item, list):
                result.append(self._convert_list(item))
            else:
                result.append(item)
        return result

    def to_dict(self):
        """Конвертирует обратно в обычный dict со всеми вложенными структурами"""
        result = {}
        for key, value in self.items():
            if isinstance(value, CaseInsensitiveDict):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = self._list_to_dict(value)
            else:
                result[key] = value
        return result

    def _list_to_dict(self, lst):
        """Рекурсивно конвертирует списки"""
        result = []
        for item in lst:
            if isinstance(item, CaseInsensitiveDict):
                result.append(item.to_dict())
            elif isinstance(item, list):
                result.append(self._list_to_dict(item))
            else:
                result.append(item)
        return result

    def __contains__(self, k):
        return k.lower() in self.proxy

    def __getitem__(self, k):
        key = self.proxy[k.lower()]
        return super().__getitem__(key)

    def get(self, k, default=None):
        return self[k] if k in self else default

    def __setitem__(self, k, v):
        # Преобразуем значение если это dict
        if isinstance(v, dict):
            v = CaseInsensitiveDict(v)
        elif isinstance(v, list):
            v = self._convert_list(v)

        lower_k = k.lower()
        if lower_k in self.proxy:
            # Обновляем существующий ключ
            original_key = self.proxy[lower_k]
            super().__setitem__(original_key, v)
        else:
            # Добавляем новый ключ
            self.proxy[lower_k] = k
            super().__setitem__(k, v)

    def __delitem__(self, k):
        lower_k = k.lower()
        if lower_k in self.proxy:
            key = self.proxy[lower_k]
            super().__delitem__(key)
            del self.proxy[lower_k]
