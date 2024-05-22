
### User Registration

**Request:**
```json
{
    "user": {
        "username": "string",
        "email": "string",
        "password": "string"
    },
    "user_type": "string"  // e.g., "influencer" or "agency"
}
```

### User Login

**Request:**
```json
{
    "username": "string",
    "password": "string"
}
```

### Token Refresh

**Response:**
```json
{
    "refresh": "string"
}
```

### Influencer Profile

**Request/Response:**
```json
{
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "mobile_number": "string",
    "gender": "string",
    "birthday_date": "string",
    "language": "string",
    "category": "string",
    "city": "string",
    "postcode": "string",
    "address": "string",
    "country": "string",
    "bio": "string",
    "facebook_link": "string",
    "twitter_link": "string",
    "instagram_link": "string",
    "Youtube_link": "string",
    "profile_pic": "string"
}
```

### Agency Profile

**Request/Response:**
```json
{
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "company_name": "string",
    "contact_person_name": "string",
    "mobile_number": "string",
    "website": "string",
    "category": "string",
    "address": "string",
    "brand_logo": "string",
    "country": "string",
    "facebook_link": "string",
    "twitter_link": "string",
    "instagram_link": "string"
}
```

### Categories

**Request/Response:**
```json
{
    "name": "string"
}
```

### Tags

**Request/Response:**
```json
{
    "name": "string"
}
```

### Post

**Request:**
```json
{
    "title": "string",
    "content": "string",
    "excerpt": "string",
    "status": "string",
    "categories": [1, 2],
    "tags": [1, 2],
    "featured_image": "string"
}
```

### Comments

**Request:**
```json
{
    "post": 1,
    "content": "string"
}
```

### Services

**Request:**
```json
{
    "user": 1,
    "category": "string",
    "title": "string",
    "price": 100,
    "tags": ["Tag1", "Tag2"],
    "description": "string",
    "status": "string",
    "images": [
        {"image": "string"},
        {"image": "string"}
    ]
}
```
