# Frontend Language Switching Examples
# This file demonstrates how frontend applications can switch languages
# when calling the Django REST API backend

# ============================================
# 1. Using HTTP Accept-Language Header
# ============================================

# English via Header
curl -X GET "http://localhost:8000/api/events/" \
  -H "Accept-Language: en" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Khmer via Header  
curl -X GET "http://localhost:8000/api/events/" \
  -H "Accept-Language: km" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# ============================================
# 2. Using Query Parameter
# ============================================

# English via Query Parameter
curl -X GET "http://localhost:8000/api/events/?lang=en" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Khmer via Query Parameter
curl -X GET "http://localhost:8000/api/events/?lang=km" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# ============================================
# 3. JavaScript/axios Examples
# ============================================

// English via Accept-Language header
const getEventsInEnglish = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/events/', {
      headers: {
        'Accept-Language': 'en',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    console.log(response.data.message); // "Events retrieved successfully."
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

// Khmer via Accept-Language header
const getEventsInKhmer = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/events/', {
      headers: {
        'Accept-Language': 'km',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    console.log(response.data.message); // "ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។"
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

// English via query parameter
const getEventsInEnglishQueryParam = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/events/?lang=en', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    console.log(response.data.message); // "Events retrieved successfully."
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

// Khmer via query parameter
const getEventsInKhmerQueryParam = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/events/?lang=km', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    console.log(response.data.message); // "ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។"
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

// ============================================
// 4. React Component Example
# ============================================

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EventList = () => {
  const [events, setEvents] = useState([]);
  const [language, setLanguage] = useState('en');
  const [message, setMessage] = useState('');

  const fetchEvents = async (lang) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/events/?lang=${lang}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setEvents(response.data.data);
      setMessage(response.data.message);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  useEffect(() => {
    fetchEvents(language);
  }, [language]);

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
  };

  return (
    <div>
      <div className="language-switcher">
        <button onClick={() => handleLanguageChange('en')}>
          English
        </button>
        <button onClick={() => handleLanguageChange('km')}>
          ខ្មែរ
        </button>
      </div>
      
      <h2>{message}</h2>
      
      <div className="events-list">
        {events.map(event => (
          <div key={event.id} className="event-card">
            <h3>{event.event_name}</h3>
            <p>{event.description}</p>
            <p><strong>Location:</strong> {event.location}</p>
            <p><strong>Date:</strong> {event.event_date}</p>
            <p><strong>Status:</strong> {event.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventList;

// ============================================
# 5. Vue.js Component Example
# ============================================

<template>
  <div>
    <div class="language-switcher">
      <button @click="setLanguage('en')">English</button>
      <button @click="setLanguage('km')">ខ្មែរ</button>
    </div>
    
    <h2>{{ message }}</h2>
    
    <div class="events-list">
      <div v-for="event in events" :key="event.id" class="event-card">
        <h3>{{ event.event_name }}</h3>
        <p>{{ event.description }}</p>
        <p><strong>Location:</strong> {{ event.location }}</p>
        <p><strong>Date:</strong> {{ event.event_date }}</p>
        <p><strong>Status:</strong> {{ event.status }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EventList',
  data() {
    return {
      events: [],
      language: 'en',
      message: ''
    };
  },
  methods: {
    async fetchEvents() {
      try {
        const response = await axios.get(`http://localhost:8000/api/events/?lang=${this.language}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.events = response.data.data;
        this.message = response.data.message;
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    },
    setLanguage(lang) {
      this.language = lang;
      this.fetchEvents();
    }
  },
  mounted() {
    this.fetchEvents();
  }
};
</script>

// ============================================
# 6. Angular Service Example
# ============================================

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EventService {
  private apiUrl = 'http://localhost:8000/api/events/';
  private token = localStorage.getItem('token') || '';

  constructor(private http: HttpClient) {}

  getEvents(language: string = 'en'): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.token}`,
      'Accept-Language': language
    });

    return this.http.get(this.apiUrl, { headers });
  }

  getEventsWithQueryParam(language: string = 'en'): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.token}`
    });

    return this.http.get(`${this.apiUrl}?lang=${language}`, { headers });
  }
}

// ============================================
# 7. Language Priority Order
# ============================================

/*
The backend language switching follows this priority order:

1. Query Parameter (?lang=km or ?lang=en) - HIGHEST PRIORITY
2. Accept-Language Header (Accept-Language: km or Accept-Language: en)
3. Default language from settings (LANGUAGE_CODE = 'en')

Examples:
- ?lang=km + Accept-Language: en = Khmer (query param wins)
- ?lang=en + Accept-Language: km = English (query param wins)
- No query param + Accept-Language: km = Khmer (header wins)
- No query param + Accept-Language: en = English (header wins)
- No query param + Accept-Language: fr = English (fallback to default)
*/

// ============================================
# 8. Complete API Response Examples
# ============================================

/*
English Response Example:
{
  "success": true,
  "message": "Events retrieved successfully.",
  "data": [
    {
      "id": 1,
      "event_name": "Tech Conference 2024",
      "description": "Annual technology conference",
      "location": "Phnom Penh",
      "event_date": "2024-03-15",
      "status": "planned"
    }
  ]
}

Khmer Response Example:
{
  "success": true,
  "message": "ទាញយកព្រឹត្តិការណ៍ដោយជោគជ័យ។",
  "data": [
    {
      "id": 1,
      "event_name": "Tech Conference 2024",
      "description": "Annual technology conference",
      "location": "Phnom Penh",
      "event_date": "2024-03-15",
      "status": "planned"
    }
  ]
}

Error Response Example (English):
{
  "success": false,
  "message": "Event not found.",
  "data": null
}

Error Response Example (Khmer):
{
  "success": false,
  "message": "រកមិនឃើញព្រឹត្តិការណ៍។",
  "data": null
}
*/
