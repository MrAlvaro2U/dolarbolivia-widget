import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Dimensions, ScrollView, ActivityIndicator } from 'react-native';
import { LineChart } from 'react-native-chart-kit';

export default function App() {
  const [precio, setPrecio] = useState(null);
  const [loading, setLoading] = useState(true);

  // Simulación de historial
  const historial = [
    16.10, 16.12, 16.15, 16.18, 16.25, 16.27, 16.30, 16.32
  ];

  useEffect(() => {
    fetch('https://mralvaro2u.github.io/dolarbolivia-widget/dolarbolivia.json')
      .then(response => response.json())
      .then(data => {
        setPrecio(data.precio_dolar_compra);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching price:', error);
        setLoading(false);
      });
  }, []);

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.titulo}>Dólar Paralelo en Bolivia</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#007AFF" />
      ) : (
        <Text style={styles.precio}>Bs {precio ?? 'No disponible'}</Text>
      )}

      <Text style={styles.subtitulo}>Historial reciente</Text>

      <LineChart
        data={{
          labels: ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"],
          datasets: [
            {
              data: historial
            }
          ]
        }}
        width={Dimensions.get("window").width - 32}
        height={220}
        yAxisSuffix=" Bs"
        chartConfig={{
          backgroundColor: "#ffffff",
          backgroundGradientFrom: "#ffffff",
          backgroundGradientTo: "#ffffff",
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(0, 122, 255, ${opacity})`,
          labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
          propsForDots: {
            r: "4",
            strokeWidth: "2",
            stroke: "#007AFF"
          }
        }}
        bezier
        style={styles.chart}
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 60,
    paddingHorizontal: 16,
    backgroundColor: '#fff',
    flex: 1
  },
  titulo: {
    fontSize: 24,
    fontWeight: '600',
    marginBottom: 8,
    color: '#000',
    textAlign: 'center'
  },
  precio: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#007AFF',
    textAlign: 'center',
    marginVertical: 16
  },
  subtitulo: {
    fontSize: 18,
    marginBottom: 8,
    fontWeight: '500',
    color: '#333'
  },
  chart: {
    borderRadius: 16,
    marginVertical: 16
  }
});
