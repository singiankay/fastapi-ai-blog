class DBUtils:

    def paginate(page, per_page):
        offset = page - 1

        return {
            "offset": offset,
            "limit": per_page
        }
