

def latest_date_in_dataframe(date_field):

    def aux(df):
        return df.sort_values(date_field, ascending=False).iloc[0]

    return aux
