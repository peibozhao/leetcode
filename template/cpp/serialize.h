
#include <iostream>
#include <string>
#include <vector>

template <typename T>
struct HasToString {
private:
  template <typename U>
  static auto Check(int)
      -> decltype(std::to_string(std::declval<U>()), std::true_type());
  template <typename U>
  static std::false_type Check(...);

public:
  enum { value = std::is_same<decltype(Check<T>(0)), std::true_type>::value };
};

std::string Trim(const std::string &s) {
  std::string ret(s);
  return ret.erase(0, ret.find_first_not_of(' '))
      .erase(ret.find_last_not_of(' ') + 1);
}

// Serialize
template <typename T>
void Serialize(const T &v, std::string &ret) {
  if (!HasToString<T>::value) {
    std::cerr << "No Implement" << std::endl;
    exit(-1);
  }
  ret = std::to_string(v);
}

template <typename T>
void Serialize(const std::vector<T> &v, std::string &ret) {
  ret = "[";
  for (int i = 0; i < v.size(); ++i) {
    std::string cur;
    Serialize(v[i], cur);
    ret += cur;
    ret += (i == v.size() - 1) ? "" : ",";
  }
  ret += ']';
}

template <>
void Serialize<std::string>(const std::string &v, std::string &ret) {
  ret = v;
}

template <>
void Serialize<bool>(const bool &v, std::string &ret) {
  ret = v ? "true" : "false";
}

// Deserialize
template <typename T>
void Deserialize(const std::string &s, T &ret) {
  std::cerr << "No Implement" << std::endl;
  exit(-1);
}

template <typename T>
void Deserialize(const std::string &s, std::vector<T> &ret) {
  std::string str = Trim(s);
  ret.clear();
  if (str.size() == 2) {
    return;
  }
  int start = 1, end = 1;
  while (end < str.size() - 1) {
    int need_match = 0;
    while (end < str.size() - 1) {
      if (str[end] == ']') {
        need_match -= 1;
      } else if (str[end] == '[') {
        need_match += 1;
      } else if (str[end] == ',' && need_match == 0) {
        break;
      }
      end += 1;
    }
    T cur;
    Deserialize(str.substr(start, end - start), cur);
    end += 1;
    start = end;
    ret.emplace_back(cur);
  }
}

template <>
void Deserialize<int>(const std::string &s, int &ret) {
  std::string str = Trim(s);
  ret = std::stoi(str);
}

template <>
void Deserialize<std::string>(const std::string &s, std::string &ret) {
  std::string str = Trim(s);
  ret = str.substr(1, str.size() - 2);
}

