import teradataml as tdml
import io
from IPython.display import Image

def plotcurves(df, field='calculated_resistance', row_axis='time_no_unit', series_id='curve_id', select_id='310096683'):
    if isinstance(select_id, list):
        if len(series_id) > 0:
            filter_ = f"WHERE {series_id} IN ({','.join([str(x) for x in select_id])}),"
        else:
            filter_ = ','
    else:
        if select_id is not None:
            filter_ = f"WHERE {series_id} = {select_id},"
        else:
            filter_ = ','

    query = f"""
    EXECUTE FUNCTION
        TD_PLOT(
            SERIES_SPEC(
            TABLE_NAME({df._table_name}),
            ROW_AXIS(SEQUENCE({row_axis})),
            SERIES_ID({series_id}),
            PAYLOAD (
                FIELDS({field}),
                CONTENT(REAL)
            )
        )
        {filter_}
        FUNC_PARAMS(
        TITLE('{field}'),
        PLOTS[(
        TYPE('line'),
        FORMAT('r')
        )],
        WIDTH(1024),
        HEIGHT(768)
        )
        );
    """

    if tdml.display.print_sqlmr_query:
        print(query)

    res = tdml.get_context().execute(query).fetchall()

    stream_str = io.BytesIO(res[0][2])

    return Image(stream_str.getvalue())

def plotcurvescluster(df, cluster, no_cluster, schema, field='calculated_resistance', row_axis='time_no_unit', series_id='CURVE_ID', select_id=None):

    tdml.copy_to_sql(df=cluster,table_name='cluster_temp',if_exists='replace',schema_name=schema)

    df_cluster = tdml.DataFrame(tdml.in_schema(schema,'cluster_temp'))
    df_select = df.join(df_cluster[df_cluster.cluster == no_cluster], how='inner', on=f'{series_id}=CURVE_ID', rsuffix='r',
                        lsuffix='l')
    df_select = df_select.assign(**{series_id: df_select['l_' + series_id]}).drop(
        columns=[f'l_{series_id}', 'r_CURVE_ID'])
    df_select.shape


    return plotcurves(df_select,field=field, row_axis=row_axis, series_id=series_id,select_id=select_id)
