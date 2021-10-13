class BandIdentifier:
    def __init__(self):
        pass

    def find_bands(self, clusters):
        centers = [round(center[0], 10) for center in clusters.cluster_centers_]

        sorted_centers = sorted(centers)

        differences = np.diff(sorted_centers)

        mean_difference = np.mean(differences)

        previous_center = 0

        for center in sorted_centers:
            difference = center - previous_center

            if difference < (mean_difference * 0.4):
                sorted_centers.remove(center)

            previous_center = center

        possible_bands = self.identify_possible_bands(sorted_centers, 0.1)

        if len(possible_bands) < 10:

            deviation = 0.11

            while len(possible_bands) < 3 and deviation < 0.3:

                possible_bands = self.identify_possible_bands(sorted_centers, deviation)

                deviation += 0.01

        if possible_bands:
            return self.most_frequent_bands(possible_bands)

        else:
            return None