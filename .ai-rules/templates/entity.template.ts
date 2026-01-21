/**
 * Template: Entity
 * 
 * Entidades têm identidade e podem mudar ao longo do tempo.
 * 
 * Regras:
 * - Deve ter um ID único
 * - Encapsula comportamento relacionado ao domínio
 * - Valida invariantes no construtor e métodos
 * - Não deve depender de infraestrutura
 */

import { Entity } from '@core/domain/base/entity.base';
import { UniqueEntityId } from '@core/domain/value-objects/unique-entity-id.vo';

// Value Objects específicos desta entidade
import { /* ValueObjects */ } from '../value-objects';

// Domain Events
import { /* Events */ } from '../events';

// Erros de domínio
import { /* Errors */ } from '../errors';

// Props da entidade
interface __ENTITY_NAME__Props {
  // Defina as propriedades aqui
  // name: string;
  // status: __ENTITY_NAME__Status;
  // createdAt: Date;
}

// Props para criar nova entidade
interface Create__ENTITY_NAME__Props {
  // Props obrigatórias para criação
  // name: string;
}

export class __ENTITY_NAME__ extends Entity<__ENTITY_NAME__Props> {
  // ==========================================
  // Getters (acesso controlado às propriedades)
  // ==========================================
  
  get name(): string {
    return this.props.name;
  }
  
  // get status(): __ENTITY_NAME__Status {
  //   return this.props.status;
  // }
  
  // ==========================================
  // Factory Methods
  // ==========================================
  
  /**
   * Cria uma NOVA entidade (gera ID)
   */
  public static create(props: Create__ENTITY_NAME__Props): __ENTITY_NAME__ {
    // Validações
    // if (!props.name) {
    //   throw new InvalidNameError();
    // }
    
    const entity = new __ENTITY_NAME__(
      {
        ...props,
        // status: __ENTITY_NAME__Status.ACTIVE,
        // createdAt: new Date(),
      },
      new UniqueEntityId(), // Novo ID
    );
    
    // Emitir evento de domínio
    // entity.addDomainEvent(new __ENTITY_NAME__CreatedEvent(entity));
    
    return entity;
  }
  
  /**
   * Reconstitui entidade existente (usa ID existente)
   * Usado pelos repositórios ao carregar do banco
   */
  public static reconstitute(
    props: __ENTITY_NAME__Props,
    id: UniqueEntityId,
  ): __ENTITY_NAME__ {
    return new __ENTITY_NAME__(props, id);
  }
  
  // ==========================================
  // Comportamentos de Domínio
  // ==========================================
  
  /**
   * Exemplo de método que muda estado
   */
  // public changeName(newName: string): void {
  //   if (!newName) {
  //     throw new InvalidNameError();
  //   }
  //   this.props.name = newName;
  //   this.addDomainEvent(new __ENTITY_NAME__NameChangedEvent(this));
  // }
  
  /**
   * Exemplo de método que valida regra de negócio
   */
  // public canBeDeleted(): boolean {
  //   return this.props.status !== __ENTITY_NAME__Status.PROCESSING;
  // }
  
  // ==========================================
  // Construtor Privado
  // ==========================================
  
  private constructor(props: __ENTITY_NAME__Props, id: UniqueEntityId) {
    super(props, id);
  }
}
