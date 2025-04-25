""" This class is advanced search methods """

class AdvancedSearchMethods:
    @staticmethod
    def is_after_date(date, date_from) -> bool:
        """
        parameters: 
        date: {
            when: (tuple of ints: (year, month, day)),
                OR
            from: (tuple of ints: (year, month, day)),
            to: (tuple of ints: (year, month, day)),

                AND
            cert: 'high', 'medium', 'low'
        
        } , 
        date_from (tuple of ints: (year, month, day))

        assume date_from is not None

        date value is in the form of a tuple of ints: (year, month, date)
        #date_from param always has all 3 ints
        keep in mind some dates in the json file only have the year and month or even just the year
        returns true for dates after and including date_from
        """
        # write code here
        #year, month, day
        #0000 00 00
        #2^7, 2^3, 2^1
        if not date: return False
        if isinstance(date, dict):
            
            when_val = date.get('when')
            if when_val:
                return AdvancedSearchMethods.is_after_date(when_val, date_from)
            from_val = date.get('from')
            to_val = date.get('to')
            if from_val and to_val:
                return AdvancedSearchMethods.is_after_date(from_val, date_from) or AdvancedSearchMethods.is_after_date(to_val, date_from)
            if from_val:
                return AdvancedSearchMethods.is_after_date(from_val, date_from)
            if to_val:
                return AdvancedSearchMethods.is_after_date(to_val, date_from)
            return False
        
        date = [int(part) for part in date.split('-')]
        date_int = 0
        date_int += date[0] << 7
        if len(date) > 1:
            date_int += date[1] << 3
            if len(date) > 2:
                date_int += date[2]
        date_from_int = (date_from[0] << 7) + (date_from[1] << 3) + (date_from[2])
        return date_int >= date_from_int

    @staticmethod
    def is_before_date(date, date_to) -> bool:
        """
        parameters: date (tuple of ints: (year, month, day)), date_to (tuple of ints: (year, month, day))
        assume date_to is not None

        date value is in the form of a tuple of ints: (year, month, day)
        keep in mind some dates only have the year and month or even just the year
        returns true for dates before and including date_to
        """
        # compares every entry to find if the user entered date is before 
        # return true if date is less than date_to
        #year, month, day
        #0000 00 00
        #2^7, 2^3, 2^1
        if not date: return False
        if isinstance(date, dict):
            when_val = date.get('when')
            if when_val:
                return AdvancedSearchMethods.is_before_date(when_val, date_to)
            from_val = date.get('from')
            to_val = date.get('to')
            if from_val and to_val:
                return AdvancedSearchMethods.is_before_date(to_val, date_to) or AdvancedSearchMethods.is_before_date(from_val, date_to)
            if to_val:
                return AdvancedSearchMethods.is_before_date(to_val, date_to)
            if from_val:
                return AdvancedSearchMethods.is_before_date(from_val, date_to)
            return False

        date = [int(part) for part in date.split('-')]
        date_int = 0
        date_int += date[0] << 7
        if len(date) > 1:
            date_int += date[1] << 3
            if len(date) > 2:
                date_int += date[2]
        date_to_int = (date_to[0] << 7) + (date_to[1] << 3) + (date_to[2])
        return date_int <= date_to_int