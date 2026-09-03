import { Hono } from 'hono'
const app = new Hono()

app.get('/', c => {
    return c.text('my vercel tiny apis')
})

export default app
