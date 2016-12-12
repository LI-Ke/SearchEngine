package upmc.ri.utils;

public class Pair<K,V extends Comparable<V>> implements Comparable<Pair<K,V>>{
	private K key;
	private V value;
	
	
	public K getKey() {
		return key;
	}
	
	public V getValue() {
		return value;
	}

	public Pair(K key, V value) {
		super();
		this.key = key;
		this.value = value;
	}


	@Override
	public int compareTo(Pair<K, V> o) {
		return value.compareTo(o.value);
	}
	

}
