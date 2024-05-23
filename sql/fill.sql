CREATE TABLE public.stocks_customuser
(
    id  SERIAL NOT NULL PRIMARY KEY,
    email    VARCHAR(254),
    password VARCHAR(50),
    is_staff    BOOLEAN DEFAULT false,
    is_superuser    BOOLEAN DEFAULT false,
    last_login TIMESTAMP
)

GRANT ALL ON ALL TABLES IN SCHEMA public to postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

ALTER TABLE public.stocks_customuser
ALTER COLUMN password TYPE VARCHAR(254);

      export const updateOrderById = createAsyncThunk<Order, OrderRequest>('updateOrder',
    async (data) => api.order.orderUpdate(String(data.id), data.data, {
        withCredentials: true,
        headers: {
            'X-CSRFToken': document.cookie
                .split('; ')
                .filter(row => row.startsWith('csrftoken='))
                .map(c => c.split('=')[1])[0],
        },
    }).then(({data}) => data));
