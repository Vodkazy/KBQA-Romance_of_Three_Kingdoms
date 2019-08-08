package edu.nju.ws.bean;

import java.util.Objects;

/**
 * 实体/属性 查询和建索引的基本单位
 */
public class Entity {
    public String IRI; //若为literal，则为lable原型
    public String lable; //包含标识符、中文名称等
    public String type; //指明类型，包括实体/属性 （人物/地点/官爵/政权/章回/事件/战争/郡/县/其他地点）

    public Entity(String IRI, String lable, String type) {
        this.IRI = IRI;
        this.lable = lable;
        this.type = type;
    }

    @Override
    public Entity clone() {
        return new Entity(this.IRI, this.lable, this.type);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Entity entity = (Entity) o;
        return Objects.equals(IRI, entity.IRI) &&
                Objects.equals(lable, entity.lable) &&
                Objects.equals(type, entity.type);
    }

    @Override
    public int hashCode() {
        return Objects.hash(IRI, lable, type);
    }

    @Override
    public String toString() {
        return "Entity{" +
                "IRI='" + IRI + '\'' +
                ", lable='" + lable + '\'' +
                ", type='" + type + '\'' +
                '}';
    }
}
