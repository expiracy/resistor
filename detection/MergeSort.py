class MergeSort:
    def __init__(self):
        pass

    def sort(self, data):
        # The last data split
        if len(data) <= 1:
            return data

        middle_index = len(data) // 2
        # Perform merge_sort recursively on both halves
        left = self.sort(data[:middle_index])
        right = self.sort(data[middle_index:])

        # Merge each side together
        return self.merge(left, right, data.copy())

    def merge(self, left, right, merged):

        left_cursor = 0
        right_cursor = 0

        while left_cursor < len(left) and right_cursor < len(right):

            # Sort each one and place into the result
            if left[left_cursor] <= right[right_cursor]:
                merged[left_cursor + right_cursor] = left[left_cursor]
                left_cursor += 1
            else:
                merged[left_cursor + right_cursor] = right[right_cursor]
                right_cursor += 1

        for left_cursor in range(left_cursor, len(left)):
            merged[left_cursor + right_cursor] = left[left_cursor]

        for right_cursor in range(right_cursor, len(right)):
            merged[left_cursor + right_cursor] = right[right_cursor]

        return merged

# Driver Code
if __name__ == '__main__':
    data = [12, 11, 13, 5, 6, 7, 4, 2, 1, 10]

    data = MergeSort().sort(data)

    print(data)




