<template>
  <div class="weather-app">
    <h1>Hava Durumu</h1>
    
    <div class="search-container">
      <input 
        v-model="city" 
        @keyup.enter="getWeather"
        placeholder="Şehir adı girin..."
        class="search-input"
      >
      <button @click="getWeather" class="search-button">Ara</button>
    </div>

    <div v-if="weather" class="weather-card">
      <h2>{{ capitalize(weather.city) }}</h2>
      
      <div class="weather-main">
        <div class="weather-icon">
          <img :src="`http://openweathermap.org/img/wn/${weather.current.weather[0].icon}@2x.png`" 
               :alt="weather.current.weather[0].description">
          <span class="weather-description">{{ weather.current.weather[0].description }}</span>
        </div>
        
        <div class="temperature">
          <span class="temp">{{ Math.round(weather.current.temp) }}°C</span>
          <span class="feels-like">Hissedilen: {{ Math.round(weather.current.feels_like) }}°C</span>
        </div>
      </div>

      <div class="weather-details">
        <div class="detail-item">
          <span class="detail-label">Nem</span>
          <span class="detail-value">{{ weather.current.humidity }}%</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Rüzgar</span>
          <span class="detail-value">{{ weather.current.wind_speed }} m/s</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Basınç</span>
          <span class="detail-value">{{ weather.current.pressure }} hPa</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Görüş</span>
          <span class="detail-value">{{ (weather.current.visibility / 1000).toFixed(1) }} km</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">UV İndeksi</span>
          <span class="detail-value">{{ weather.current.uvi }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Bulut</span>
          <span class="detail-value">{{ weather.current.clouds }}%</span>
        </div>
      </div>

      <div class="sun-times">
        <div class="sun-item">
          <span class="sun-label">Gün Doğumu</span>
          <span class="sun-value">{{ formatTime(weather.current.sunrise) }}</span>
        </div>
        <div class="sun-item">
          <span class="sun-label">Gün Batımı</span>
          <span class="sun-value">{{ formatTime(weather.current.sunset) }}</span>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      city: '',
      weather: null,
      error: null
    }
  },
  methods: {
    async getWeather() {
      if (!this.city) {
        this.error = 'Lütfen bir şehir adı girin'
        return
      }

      try {
        this.error = null
        const response = await axios.post('http://localhost:8000/weather', {
          city: this.city
        })
        this.weather = response.data
      } catch (err) {
        this.error = 'Hava durumu bilgisi alınamadı. Lütfen geçerli bir şehir adı girin.'
        this.weather = null
      }
    },
    formatTime(timestamp) {
      const date = new Date(timestamp * 1000)
      return date.toLocaleTimeString('tr-TR', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false 
      })
    },
    capitalize(str) {
      if (!str) return '';
      return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    }
  },
  async mounted() {
    try {
      const response = await axios.get('http://localhost:8000/weather/default')
      this.weather = response.data
    } catch (err) {
      this.error = 'Varsayılan hava durumu bilgisi alınamadı'
    }
  }
}
</script>

<style>
.weather-app {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.search-container {
  margin: 20px 0;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.search-input {
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.search-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #3aa876;
}

.weather-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.weather-main {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin: 20px 0;
}

.weather-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.weather-icon img {
  width: 80px;
  height: 80px;
}

.weather-description {
  text-transform: capitalize;
  color: #666;
}

.temperature {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.temp {
  font-size: 48px;
  font-weight: bold;
  color: #2c3e50;
}

.feels-like {
  font-size: 18px;
  color: #666;
}

.weather-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin: 20px 0;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.detail-label {
  font-size: 14px;
  color: #666;
}

.detail-value {
  font-size: 18px;
  font-weight: 500;
  color: #2c3e50;
}

.sun-times {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.sun-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.sun-label {
  font-size: 14px;
  color: #666;
}

.sun-value {
  font-size: 16px;
  font-weight: 500;
  color: #2c3e50;
}

.error-message {
  color: #dc3545;
  margin-top: 20px;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
}
</style>
