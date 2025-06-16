import React, { useEffect, useState } from 'react';
import { Text, View, StyleSheet, ActivityIndicator } from 'react-native';

export default function App() {
  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://mralvaro2u.github.io/dolar-widget-data/dolarbolivia.json')
      .then((response) => response.json())
      .then((data) => {
        setPrice(data.precio_dolar_compra);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching price:', error);
        setLoading(false);
      });
  }, []);

  return (
    <View style={styles.container}>
      {loading ? (
        <ActivityIndicator size="large" />
      ) : (
        <Text style={styles.text}>Precio del dólar: {price} Bs</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  text: { fontSize: 24 },
});
