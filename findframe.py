
class Frame:
    """class to hold information about each frame

    """

    def __init__(self, id, diff):
        self.id = id
        self.diff = diff

    def __lt__(self, other):
        if self.id == other.id:
            return self.id < other.id
        return self.id < other.id

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return self.id == other.id and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def getMAXdiff(self, list=[]):
        """
        find the max_diff_frame in the window

        """
        LIST = list[:]
        temp = LIST[0]
        for i in range(0,len(LIST)):
            if temp.diff > LIST[i].diff:
                continue
            else:
                temp = LIST[i]

        return temp

    def find_possible_frame(self, list_frames):
        """
        detect the possible frame

        """
        possible_frame = []
        window_frame = []
        window_size = 30
        m_suddenJudge = 3
        m_MinLengthOfShot = 8
        start_id_spot = []
        start_id_spot.append(0)
        end_id_spot = []

        length = len(list_frames)
        index = 0
        while(index < length):
            frame_item = list_frames[index]
            window_frame.append(frame_item)
            if len(window_frame) < window_size:
                index += 1
                if index == length-1:
                    window_frame.append(list_frames[index])
                else:
                    continue

            # find the max_diff_frame
            max_diff_frame = self.getMAXdiff(window_frame)
            max_diff_id = max_diff_frame.id

            if len(possible_frame) == 0:
                possible_frame.append(max_diff_frame)
                continue
            last_max_frame = possible_frame[-1]

            """
            
            Check whether the difference of the selected frame is more than 3 times the average difference of the other frames in the window.
            
            """

            sum_start_id = last_max_frame.id + 1
            sum_end_id = max_diff_id - 1


            id_no = sum_start_id
            sum_diff = 0
            while True:

                sum_frame_item = list_frames[id_no]
                sum_diff += sum_frame_item.diff
                id_no += 1
                if id_no > sum_end_id:
                    break

            average_diff = sum_diff / (sum_end_id - sum_start_id + 1)
            if max_diff_frame.diff >= (m_suddenJudge * average_diff):
                possible_frame.append(max_diff_frame)
                window_frame = []
                index = possible_frame[-1].id + m_MinLengthOfShot
                continue
            else:
                index = max_diff_frame.id + 1
                window_frame = []
                continue

        """
        
        get the index of the first and last frame of a shot
        
        """
        for i in range(0, len(possible_frame)):
            start_id_spot.append(possible_frame[i].id)
            end_id_spot.append(possible_frame[i].id - 1)


        sus_last_frame = possible_frame[-1]
        last_frame = list_frames[-1]
        if sus_last_frame.id < last_frame.id:
            possible_frame.append(last_frame)
            end_id_spot.append(possible_frame[-1].id)

        return possible_frame, start_id_spot, end_id_spot

    def optimize_frame(self, tag_frames, list_frames):
        '''

            optimize the possible frame

        '''
        new_tag_frames = []
        frame_count = 10
        diff_threshold = 10
        diff_optimize = 2
        start_id_spot = []
        start_id_spot.append(0)
        end_id_spot = []

        for tag_frame in tag_frames:

            tag_id = tag_frame.id

            """
            
            check whether the difference of the possible frame is no less than 10.
            
            """
            if tag_frame.diff < diff_threshold:
                continue
            """
            
            check whether the difference is more than twice the average difference of 
            the previous 10 frames and the subsequent 10 frames.
            
            """
            #get the previous 10 frames
            pre_start_id = tag_id - frame_count
            pre_end_id = tag_id - 1
            if pre_start_id < 0:
                continue

            pre_sum_diff = 0
            check_id = pre_start_id
            while True:
                pre_frame_info = list_frames[check_id]
                pre_sum_diff += pre_frame_info.diff
                check_id += 1
                if check_id > pre_end_id:
                    break

            #get the subsequent 10 frames
            back_start_id = tag_id + 1
            back_end_id = tag_id + frame_count
            if back_end_id >= len(list_frames):
                continue

            back_sum_diff = 0
            check_id = back_start_id
            while True:
                back_frame_info = list_frames[check_id]
                back_sum_diff += back_frame_info.diff
                check_id += 1
                if check_id > back_end_id:
                    break

            # calculate the difference of the previous 10 frames and the subsequent 10 frames
            sum_diff = pre_sum_diff + back_sum_diff
            average_diff = sum_diff / (frame_count * 2)

            #check whether the requirement is met or not
            if tag_frame.diff > (diff_optimize * average_diff):
                new_tag_frames.append(tag_frame)

        """

        get the index of the first and last frame of a shot

        """

        for i in range(0,len(new_tag_frames)):
            start_id_spot.append(new_tag_frames[i].id)
            end_id_spot.append(new_tag_frames[i].id - 1)


        last_frame = list_frames[-1]
        if new_tag_frames[-1].id < last_frame.id:
            new_tag_frames.append(last_frame)

        end_id_spot.append(new_tag_frames[-1].id)


        return new_tag_frames, start_id_spot, end_id_spot
