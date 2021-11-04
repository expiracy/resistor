class MergeSort:
    def __init__(self):
        pass

    # Sorts input data.
    def sort(self, data, reverse=False):
        # The last data split
        if len(data) <= 1:
            return data

        middle_index = len(data) // 2
        # Perform merge_sort recursively on both halves
        left = self.sort(data[:middle_index])
        right = self.sort(data[middle_index:])

        # Merge each side together
        merged = self.merge(left, right, data.copy(), reverse)

        return merged

    # Merges and sorts a list.
    def merge(self, left, right, merged, reverse):
        left_cursor = 0
        right_cursor = 0

        while left_cursor < len(left) and right_cursor < len(right):

            if reverse:
                # Sort each one and place into the result
                if left[left_cursor] >= right[right_cursor]:
                    merged[left_cursor + right_cursor] = left[left_cursor]
                    left_cursor += 1
                else:
                    merged[left_cursor + right_cursor] = right[right_cursor]
                    right_cursor += 1

            else:
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

    def split(self, data):
        middle_index = len(data) // 2

        if len(data) <= 1:
            return data

        left = data[:middle_index]
        right = data[middle_index:]

        return left, right

    def sorting(self, left, right=None):

        while len(left) > 1:
            pass


if __name__ == "__main__":
    MergeSort().split([38, 27, 43, 3, 9, 82, 10])
