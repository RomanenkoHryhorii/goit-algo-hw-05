def binary_search_float(arr, target, tolerance=1e-9):
    """
    Виконує двійковий пошук у відсортованому масиві дробових чисел.
    
    Параметри:
    arr (list): Відсортований масив дробових чисел
    target (float): Значення, яке потрібно знайти
    tolerance (float): Допустима похибка для порівняння дробових чисел
    
    Повертає:
    tuple: (кількість ітерацій, верхня межа)
    """
    left, right = 0, len(arr) - 1
    iterations = 0
    
    # Додаткова перевірка меж масиву
    if len(arr) == 0:
        return (0, None)
    
    # Перевірка меж діапазону
    if target < arr[0]:
        return (0, arr[0])
    
    if target > arr[-1]:
        return (len(arr), None)
    
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        # Точне співставлення з урахуванням допустимої похибки
        if abs(arr[mid] - target) < tolerance:
            return (iterations, arr[mid])
        
        # Якщо поточний елемент менший за ціль
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    # Знаходження верхньої межі
    for i in range(left, len(arr)):
        if arr[i] >= target:
            return (iterations, arr[i])
    
    return (iterations, None)

# Приклад використання
def main():
    # Тестові випадки
    test_cases = [
        ([1.1, 2.2, 3.3, 4.4, 5.5], 3.0),   # Пошук наближеного значення
        ([1.1, 2.2, 3.3, 4.4, 5.5], 2.2),   # Точне співставлення
        ([1.1, 2.2, 3.3, 4.4, 5.5], 6.0),   # Значення поза межами масиву
        ([1.1, 2.2, 3.3, 4.4, 5.5], 0.5),   # Значення менше за найменший елемент
        ([], 3.0)                           # Порожній масив
    ]
    
    for arr, target in test_cases:
        result = binary_search_float(arr, target)
        print(f"Пошук {target} у {arr}:")
        print(f"Результат: {result}")
        print()

if __name__ == "__main__":
    main()