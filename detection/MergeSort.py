# The merge sort algorithm.
class MergeSort:
    def __init__(self):
        pass

    # Responsible for sorting and merging the lists
    def sort_and_merge_lists(self, left, right, reverse):

        left_index = 0
        right_index = 0

        sorted_and_merged_list = []

        while left_index < len(left) and right_index < len(right):

            if reverse:
                if left[left_index] > right[right_index]:
                    sorted_and_merged_list.append(left[left_index])
                    left_index += 1

                else:
                    sorted_and_merged_list.append(right[right_index])
                    right_index += 1

            else:
                if left[left_index] < right[right_index]:
                    sorted_and_merged_list.append(left[left_index])
                    left_index += 1

                else:
                    sorted_and_merged_list.append(right[right_index])
                    right_index += 1

        sorted_and_merged_list.extend(left[left_index:])
        sorted_and_merged_list.extend(right[right_index:])

        return sorted_and_merged_list

    # The entry point for the sort
    def sort(self, data, reverse=False):

        if len(data) <= 1:
            return data

        middle_index = len(data) // 2

        left = data[:middle_index]
        right = data[middle_index:]

        left = self.sort(left, reverse)
        right = self.sort(right, reverse)

        sorted_and_merged_list = self.sort_and_merge_lists(left, right, reverse)

        return sorted_and_merged_list


if __name__ == "__main__":
    print('Original:', [14, 7, 3, 12, 9, 11, 6, 2])
    sorted = MergeSort().sort([14, 7, 3, 12, 9, 11, 6, 2], False)
    print(sorted)
